## **Architecture and Folder Structure**

### **Overview**

The application is built using the **FastAPI** framework for the backend, allowing it to handle HTTP requests efficiently. The application interacts with external APIs, including an LLM (Large Language Model) service for generating creative prompts and a WebSocket-based service for generating images based on user input.

The **modular architecture** breaks the code into components based on functionality, which promotes separation of concerns, improves maintainability, and scales better as the application grows.

### **Folder Structure**

```bash
├── backend/
│   ├── __init__.py
│   ├── main.py         # Entry point for FastAPI and application startup
│   ├── routes.py       # Contains all the route definitions for the API
│   ├── services.py     # Contains the business logic, interactions with external services like LLMs, image generation, etc.
│   ├── models.py       # Defines Pydantic models like LLMRequest, PromptRequest, etc.
├── Dockerfile
├── .dockerignore
├── .env
├── .gitignore
├── Readme.md
├── requirements.txt
├── workflow.json
├── quick_prompts.json
├── ui/
│   ├── index.html
│   ├── script.js
│   ├── style.css
```

### **Why This Folder Structure?**

- **Separation of Concerns**: By splitting the application into **routes**, **services**, and **models**, each file has a focused responsibility:
  - `routes.py` handles request routing and endpoint definitions.
  - `services.py` handles the core business logic, interactions with external services, and complex operations.
  - `models.py` contains the data models that define the request and response formats.

- **Scalability**: As the application grows, this structure allows easy addition of new features without bloating any single file. For instance, adding new routes can be done by simply extending `routes.py` without touching the core logic in `services.py`.

- **Reusability**: The modular approach allows the business logic in `services.py` to be reused in different routes or even across multiple applications without needing to rewrite the code.

- **Maintainability**: When each file has a single responsibility, debugging and extending the application become much easier. If a bug occurs in the prompt generation, we know that we only need to investigate `services.py`. Similarly, changes to how data is structured are confined to `models.py`.

---

## **Flow of the Application**

1. **Application Entry Point** (`main.py`)
   - The **FastAPI** application is initialized in `main.py`. It serves as the entry point for the entire backend, mounting the `routes.py` via the `include_router()` function. 
   - Static files (like HTML, CSS, and JS) are mounted to serve the front-end resources.

   ```python
   app.mount("/static", StaticFiles(directory="ui"), name="static")
   ```

2. **Routing and Request Handling** (`routes.py`)
   - The `routes.py` file defines all the HTTP routes, such as:
     - `GET /`: Serves the main HTML file (`index.html`).
     - `GET /quick_prompts/`: Serves predefined prompts from the `quick_prompts.json` file.
     - `POST /ask_llm/`: Handles requests to the LLM to generate creative ideas based on user input.
     - `POST /generate_images/`: Triggers the image generation process.

   - The routes define what action should be taken when the FastAPI server receives an HTTP request, but the core business logic is abstracted into `services.py`.

3. **Business Logic and External Services** (`services.py`)
   - **Core Logic**: This file handles the interactions with external services (LLM, WebSocket server) and encapsulates the complex operations.
   
   - **Why separate business logic?**: The logic of sending requests to the LLM, generating images, and fetching results from WebSocket is often intricate and should not be mixed with routing. By isolating this functionality in `services.py`, the code becomes more maintainable and reusable.

   - **LLM Interaction**: 
     - The `ask_llm_service` function interacts with the Ollama server to send a prompt and retrieve a creative response. This is done by making a POST request to the LLM service's API and processing the response.
     - The separation of this logic means you can easily change the external LLM service in the future without altering the core routing code.

     ```python
     response = requests.post(ollama_server_url, json=ollama_request, headers={"Content-Type": "application/json"})
     response_data = response.json()
     ```

   - **Image Generation**:
     - The `generate_images` function handles image generation. It connects to a WebSocket server, sends a prompt, and processes the responses, eventually returning the images in a suitable format.
     - Again, this complex operation is encapsulated in `services.py`, separating the logic from the routing layer.

4. **Data Models and Validation** (`models.py`)
   - This file defines the structure of the data used in the application, using **Pydantic** models to enforce strict validation of input.
   - **Why Pydantic models?**: They allow for automatic validation of request bodies, making the application more robust by rejecting invalid input before it even reaches the business logic.

   - **Models**:
     - `LLMRequest`: Defines the schema for a request to the LLM service, ensuring that a `positive_prompt` is provided.
     - `PromptRequest`: Defines the schema for the image generation request, ensuring that `positive_prompt`, `negative_prompt`, and other parameters (e.g., image resolution) are valid.

     ```python
     class LLMRequest(BaseModel):
         positive_prompt: str

     class PromptRequest(BaseModel):
         positive_prompt: str
         negative_prompt: str
         steps: int = 25
         width: int = 512
         height: int = 512
     ```

---

## **Request-Response Flow**

### 1. **Frontend Request**
   - A request comes from the front-end (served from `ui/index.html`).
   - Examples:
     - When the user submits a text prompt for LLM: `POST /ask_llm/`
     - When the user requests image generation: `POST /generate_images/`

### 2. **Routing Layer** (`routes.py`)
   - The incoming HTTP request is routed by FastAPI, which directs it to the appropriate endpoint handler in `routes.py`.
   - **Example**: A request to `POST /ask_llm/` is handled by the `ask_llm` function, which parses the request data and then calls the corresponding function in `services.py`.

### 3. **Business Logic Layer** (`services.py`)
   - The service layer handles the core operations:
     - If the request involves an LLM, `ask_llm_service()` sends a POST request to the LLM API.
     - If the request is for image generation, `generate_images()` opens a WebSocket connection, interacts with the image generation service, and processes the result.

### 4. **Response Generation**
   - After processing in the service layer, the results (e.g., LLM response, images) are returned to `routes.py`.
   - The route function wraps the results in a suitable response object (e.g., `JSONResponse`, `StreamingResponse`) and returns it to the frontend.
   - The front-end then updates based on the server's response.

---


This architecture and folder structure prioritize **clarity, scalability, and maintainability**. By separating the application into layers, each responsible for a single aspect of the program's functionality, we can easily add new features, modify existing functionality, and debug any issues. 

- **Routes** handle request dispatching and control the API's behavior.
- **Services** handle all the business logic and complex operations.
- **Models** ensure data consistency and validation, leading to fewer errors.
  
This modular structure also enables easier testing and deployment since each module can be tested individually without breaking the overall flow of the application.

