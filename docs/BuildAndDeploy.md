## **Running the Application with and without Docker**

This guide explains how to run the application both locally and via Docker, using the command `docker run -d -p 8000:8000 --name dreamcanvas dreamcanvas`. It also covers how to test the application via a web browser and cURL.

---

### **Running the Application Locally**

1. **Install Dependencies**:  
   Ensure you have Python and all required dependencies installed. In the root of your project directory, run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**:  
   Run the following command to start the FastAPI server using Uvicorn:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Test the Application via Browser**:  
   Open a web browser and navigate to `http://localhost:8000/docs`. This will bring up **Swagger UI**, where you can interact with the API endpoints.

4. **Test the Application via cURL**:  
   To test the `/generate_images/` endpoint, run this **cURL** command:
   ```bash
   curl 'http://localhost:8000/generate_images/' \
   -H 'Content-Type: application/json' \
   --data-raw '{
     "positive_prompt": "Pretty woman in her late 20s 4k highly detailed hyperrealistic",
     "negative_prompt": "Trees low quality blurry watermark",
     "steps": 25,
     "width": 512,
     "height": 512
   }' \
   --insecure
   ```

---

### **Running the Application with Docker**

You can also run the application inside a Docker container, which ensures a consistent environment for deployment and testing.

#### **1. Build the Docker Image**
First, ensure you have Docker installed. Navigate to your project root directory (where the `Dockerfile` is located), and run the following command to build the Docker image:

```bash
docker build -t dreamcanvas .
```

This command will create a Docker image named `dreamcanvas`.

#### **2. Run the Docker Container**
Once the image is built, you can start the application in detached mode using this command:

```bash
docker run -d -p 8000:8000 --name dreamcanvas dreamcanvas
```

- `-d` runs the container in detached mode (in the background).
- `-p 8000:8000` maps port 8000 on your host machine to port 8000 inside the Docker container, making the application accessible via `http://localhost:8000`.
- `--name dreamcanvas` assigns a name to the running container, making it easier to manage.

#### **3. Test the Application in Browser**
Open your web browser and navigate to `http://localhost:8000/docs` to access **Swagger UI**. This interface allows you to interact with all the available API endpoints.

#### **4. Test the Application via cURL**
To test the `/generate_images/` endpoint, use this **cURL** command:

```bash
curl 'http://localhost:8000/generate_images/' \
-H 'Content-Type: application/json' \
--data-raw '{
  "positive_prompt": "Pretty woman in her late 20s 4k highly detailed hyperrealistic",
  "negative_prompt": "Trees low quality blurry watermark",
  "steps": 25,
  "width": 512,
  "height": 512
}' \
--insecure
```

---

### **Stopping and Managing the Docker Container**

#### **Stop the Container**
If you need to stop the container, you can run:

```bash
docker stop dreamcanvas
```

#### **Restart the Container**
To restart the stopped container, use:

```bash
docker start dreamcanvas
```

#### **Remove the Container**
To remove the container when you're done testing, run:

```bash
docker rm -f dreamcanvas
```

This will stop and remove the container completely.
