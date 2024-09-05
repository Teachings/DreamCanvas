import websocket  # websocket-client
import uuid
import json
import urllib.request
import urllib.parse
import random
from PIL import Image
import io
from termcolor import colored
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get server address from environment variable, default to "localhost:8188" if not set
server_address = os.getenv('COMFYUI_SERVER_ADDRESS', 'localhost:8188')
client_id = str(uuid.uuid4())

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
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}

    last_reported_percentage = 0

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'progress':
                data = message['data']
                current_progress = data['value']
                max_progress = data['max']
                percentage = int((current_progress / max_progress) * 100)

                # Only update progress every 10%
                if percentage >= last_reported_percentage + 10:
                    print(colored(f"Progress: {percentage}% in node {data['node']}", "yellow"))
                    last_reported_percentage = percentage

            elif message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    print(colored("Execution complete.", "green"))
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
def generate_images(positive_prompt, negative_prompt, steps=25, resolution=(512, 512)):
    # Open WebSocket connection
    ws = websocket.WebSocket()
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
    images = get_images(ws, workflow)

    # Close WebSocket connection
    ws.close()

    return images, seed

# Example of calling the method and saving the images
if __name__ == "__main__":
    # User input for prompts
    positive_prompt = input(colored("Enter the positive prompt: ", "cyan"))
    negative_prompt = input(colored("Enter the negative prompt: ", "cyan"))

    # Call the generate_images function
    images, seed = generate_images(positive_prompt, negative_prompt)

    # Save the images
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            image.save(f"outputs/{node_id}-{seed}.png")
            print(colored(f"Image saved as outputs/{node_id}-{seed}.png", "blue"))
