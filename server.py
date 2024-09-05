import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import websocket as ws_client
import uuid
import json
import urllib.request
import urllib.parse
import random
from PIL import Image
import io
from typing import List
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get server address from environment variable, default to "localhost:8188" if not set
server_address = os.getenv('COMFYUI_SERVER_ADDRESS', 'localhost:8188')
client_id = str(uuid.uuid4())
ollama_server_address = os.getenv('OLLAMA_SERVER_ADDRESS', 'localhost:11434')
ollama_server_url = f"http://{ollama_server_address}/v1/chat/completions"

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="ui"), name="static")

# Serve HTML file (index.html)
@app.get("/")
async def get_index():
    return FileResponse("ui/index.html")

# Endpoint to serve quick prompts from configuration file
@app.get("/quick_prompts/")
async def get_quick_prompts():
    try:
        with open("quick_prompts.json", "r") as f:
            prompts = json.load(f)
        return JSONResponse(content=prompts)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading quick prompts file.")

# Endpoint to ask the LLM for creative ideas based on the positive prompt
class LLMRequest(BaseModel):
    positive_prompt: str


@app.post("/ask_llm/")
async def ask_llm(request: LLMRequest):
    try:
        # Prepare the request for Ollama
        ollama_request = {
            "model": "hermes3:70b",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a creative assistant. Generate a creative image prompt based on the following input."
                },
                {
                    "role": "user",
                    "content": request.positive_prompt
                }
            ]
        }

        # Send the request to the Ollama server
        response = requests.post(ollama_server_url, json=ollama_request, headers={"Content-Type": "application/json"})
        response_data = response.json()

        # Extract the assistant's message from the response
        assistant_reply = response_data["choices"][0]["message"]["content"]

        return JSONResponse(content={"assistant_reply": assistant_reply})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interacting with LLM: " + str(e))



class PromptRequest(BaseModel):
    positive_prompt: str
    negative_prompt: str
    steps: int = 25
    width: int = 512
    height: int = 512

# Queue prompt function
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

# Get image function
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()

# Get history for a prompt ID
def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())

# Get images from the workflow
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
                    break  # Execution is done
        else:
            continue  # Previews are binary data

    # Fetch history and images after completion
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

# Generate images function with customizable input
async def generate_images(positive_prompt, negative_prompt, steps=25, resolution=(512, 512)):
    # Open WebSocket connection
    ws = ws_client.WebSocket()
    ws.connect(f"ws://{server_address}/ws?clientId={client_id}")

    # Load workflow from file
    with open("workflow.json", "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    # Set the text prompt for positive and negative CLIPTextEncode
    workflow["6"]["inputs"]["text"] = positive_prompt
    workflow["7"]["inputs"]["text"] = negative_prompt

    # Set steps for KSampler node
    workflow["3"]["inputs"]["steps"] = steps

    # Set resolution for EmptyLatentImage node
    workflow["5"]["inputs"]["width"] = resolution[0]
    workflow["5"]["inputs"]["height"] = resolution[1]

    # Set a random seed for the KSampler node
    seed = random.randint(1, 1000000000)
    workflow["3"]["inputs"]["seed"] = seed

    # Fetch generated images
    images = await get_images(ws, workflow)

    # Close WebSocket connection
    ws.close()

    return images, seed

@app.post("/generate_images/")
async def generate_images_api(request: PromptRequest):
    try:
        images, seed = await generate_images(
            request.positive_prompt,
            request.negative_prompt,
            request.steps,
            (request.width, request.height)
        )

        # Convert images to a format FastAPI can return
        image_responses = []
        for node_id in images:
            for image_data in images[node_id]:
                img = Image.open(io.BytesIO(image_data))
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)

                # Append the image response to a list
                image_responses.append(StreamingResponse(img_byte_arr, media_type="image/png"))

        return image_responses[0]  # Return the first image for simplicity, or modify to return all images

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
