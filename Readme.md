
# DreamCanvas - AI-Powered Creativity

DreamCanvas is an AI-powered image generator that allows users to create creative, high-quality images using ComfyUI and integrates with a local Large Language Model (LLM) via Ollama. This project includes a FastAPI backend, a dynamic web interface, and support for user-configurable models and servers.

---

## Table of Contents
- [Setup](#setup)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
- [Functionality](#functionality)
  - [Positive and Negative Prompts](#positive-and-negative-prompts)
  - [LLM-Assisted Prompt Generation](#llm-assisted-prompt-generation)
  - [Quick Prompts](#quick-prompts)
  - [Image Caching and Navigation](#image-caching-and-navigation)
  - [UI Reset](#ui-reset)
- [Architecture](#architecture)
  - [Backend](#backend)
    - [Key Endpoints](#key-endpoints)
  - [Frontend](#frontend)
    - [UI Components](#ui-components)
  - [Tools and Libraries](#tools-and-libraries)
- [Testing](#testing)

---

## Setup

### Requirements

1. **Conda Environment**:
   - The project uses Conda for environment management. Make sure Conda is installed on your system.

2. **ComfyUI**:
   - ComfyUI should be installed and running. You must have the checkpoint `realvisxlV50Lightning.Ng9I.safetensors` installed in the `checkpoints/models` folder for the workflow.
   - Alternatively, you can modify `workflow.json` to use any other model/checkpoint.

3. **Ollama**:
   - Ollama LLM server should be installed and accessible.

4. **Configuration via `.env`**:
   - The project uses a `.env` file for configuring server addresses:
     ```bash
     COMFYUI_SERVER_ADDRESS=192.168.1.10:8188
     OLLAMA_SERVER_ADDRESS=192.168.1.10:11436
     ```
   - Adjust these values to match your environment.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Teachings/dreamcanvas.git
   cd dreamcanvas
   ```

2. **Set Up Conda Environment**:

   Create and activate the Conda environment:

   ```bash
   conda create --name dreamcanvas python=3.12
   conda activate dreamcanvas
   ```

3. **Install Dependencies**:

   Install the project dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up `.env` File**:

   Ensure the `.env` file exists in the project root and contains the correct server addresses for ComfyUI and Ollama:

   ```bash
   COMFYUI_SERVER_ADDRESS=192.168.1.10:8188
   OLLAMA_SERVER_ADDRESS=192.168.1.10:11436
   ```

### Running the Server

Start the FastAPI server with the following command:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

This will run the app on `http://localhost:8000/`.

To test that ComfyUI is working fine, you can run `main.py`:

```bash
python main.py
```

---

## Functionality

### Positive and Negative Prompts

- **Positive Prompt**: Specify the elements that should be emphasized in the image (e.g., "4k, highly detailed, hyperrealistic").
- **Negative Prompt**: Define elements to avoid in the image (e.g., "blurry, watermark").

### LLM-Assisted Prompt Generation

- **Ask LLM for Creative Idea**: Users can click this button to ask a locally hosted LLM (Ollama) for a creative suggestion. The returned prompt can be applied directly to the positive prompt input by clicking "Use LLM's Creative Prompt."

### Quick Prompts

- **Preconfigured Prompts**: Both positive and negative quick prompts are available as buttons. Clicking a button auto-fills the corresponding input field.
- **Themed Prompts**: Themes like **Halloween** or **Christmas** are dynamically loaded from the `quick_prompts.json` file. You can easily add new themes by editing this file.

### Image Caching and Navigation

- **Image History**: The app caches generated images locally within the session. Use the **Previous** and **Next** buttons to navigate through previously generated images.
- **Cache Clearing**: Cached images are cleared when the browser is refreshed or the **Reset** button is clicked.

### UI Reset

- **Reset Button**: Resets the entire UI, clearing all inputs, generated images, and cached history.

---

## Architecture

### Backend

The backend is powered by FastAPI and manages image generation, LLM interactions, and serving quick prompts.

#### Key Endpoints

1. **POST /generate_images/**

   - **Description**: Generates an AI image using the provided prompts and image settings.
   - **Request Example**:
     ```json
     {
       "positive_prompt": "a beautiful sunset",
       "negative_prompt": "blurry",
       "steps": 25,
       "width": 512,
       "height": 512
     }
     ```
   - **Response**: A binary stream containing the generated image.

2. **POST /ask_llm/**

   - **Description**: Requests a creative prompt from the local LLM server (Ollama).
   - **Request Example**:
     ```json
     {
       "positive_prompt": "a beautiful sunset"
     }
     ```
   - **Response**:
     ```json
     {
       "assistant_reply": "How about a stunning sunset over the mountains with golden light reflecting on the water?"
     }
     ```

3. **GET /quick_prompts/**

   - **Description**: Retrieves quick prompt configurations from the `quick_prompts.json` file for dynamic UI updates.
   - **Response Example**:
     ```json
     {
       "Positive Quick Prompts": [
         { "label": "4K", "value": "4K" },
         { "label": "Highly Detailed", "value": "highly detailed" }
       ],
       "Negative Quick Prompts": [
         { "label": "Blurry", "value": "blurry" },
         { "label": "Watermark", "value": "watermark" }
       ],
       "Halloween": [
         { "label": "Black Background", "value": "black background" },
         { "label": "Witch", "value": "witch" }
       ]
     }
     ```

### Frontend

The UI is built using HTML, CSS (Bootstrap), and JavaScript. It dynamically interacts with the backend for generating images, fetching LLM responses, and loading quick prompts.

#### UI Components

1. **Image Generation Form**:
   - Inputs for positive and negative prompts, image steps, width, and height.
   - Quick prompt buttons for adding predefined keywords.

2. **LLM Integration**:
   - A section that allows users to request and apply creative prompts from the local LLM.

3. **Image Display and Navigation**:
   - Displays generated images and includes navigation buttons to browse cached images.

4. **Reset Functionality**:
   - A **Reset** button that clears all fields, images, and the cache of generated images.

### Tools and Libraries

1. **FastAPI**: Python-based web framework for building the backend.
2. **Uvicorn**: ASGI server for running FastAPI.
3. **Ollama**: Locally hosted LLM for generating creative prompt suggestions.
4. **Pillow**: Python Imaging Library used for image handling and generation.
5. **Bootstrap**: Frontend framework for styling the UI.
6. **JavaScript (Fetch API)**: Handles API calls to the backend for image generation and LLM requests.

---

## Testing

You can test that ComfyUI is working fine using the `main.py` script:

```bash
python main.py
```

This script interacts with the ComfyUI server directly and runs a basic test workflow using the `workflow.json` file. Modify the workflow or models as needed.
