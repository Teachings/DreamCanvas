import os
import json
import requests
import random
import uuid
import websocket as ws_client
from dotenv import load_dotenv
from urllib.request import urlopen, Request
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

server_address = os.getenv('COMFYUI_SERVER_ADDRESS', 'localhost:8188')
client_id = str(uuid.uuid4())
ollama_server_address = os.getenv('OLLAMA_SERVER_ADDRESS', 'localhost:11434')
ollama_server_url = f"http://{ollama_server_address}/v1/chat/completions"
ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.1:latest')  # Load model from .env

# Service to get quick prompts data
def get_quick_prompts_data():
    with open("quick_prompts.json", "r") as f:
        return json.load(f)

# Service to ask LLM for response
def ask_llm_service(positive_prompt: str):
    ollama_request = {
        "model": ollama_model,  # Use model from .env
        "messages": [
            {
                "role": "system",
                "content": "You are a creative assistant. Generate a creative image prompt based on the following input."
            },
            {
                "role": "user",
                "content": positive_prompt
            }
        ]
    }

    response = requests.post(ollama_server_url, json=ollama_request, headers={"Content-Type": "application/json"})
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]

# Service to queue a prompt
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urlopen(req).read())

# Service to get image
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urlencode(data)
    with urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()

# Service to get history
def get_history(prompt_id):
    with urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())

# WebSocket image generation service
async def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break
        else:
            continue

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output

    return output_images

# Main image generation function
async def generate_images(positive_prompt, negative_prompt, steps=25, resolution=(512, 512)):
    ws = ws_client.WebSocket()
    ws.connect(f"ws://{server_address}/ws?clientId={client_id}")

    with open("workflow.json", "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    workflow["6"]["inputs"]["text"] = positive_prompt
    workflow["7"]["inputs"]["text"] = negative_prompt
    workflow["3"]["inputs"]["steps"] = steps
    workflow["5"]["inputs"]["width"] = resolution[0]
    workflow["5"]["inputs"]["height"] = resolution[1]
    seed = random.randint(1, 1000000000)
    workflow["3"]["inputs"]["seed"] = seed

    images = await get_images(ws, workflow)

    ws.close()

    return images, seed
