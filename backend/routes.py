from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from .models import LLMRequest, PromptRequest
from .services import generate_images, get_quick_prompts_data, ask_llm_service
from PIL import Image
import io

router = APIRouter()

# Serve HTML file (index.html)
@router.get("/")
async def get_index():
    return FileResponse("ui/index.html")

# Endpoint to serve quick prompts from configuration file
@router.get("/quick_prompts/")
async def get_quick_prompts():
    try:
        prompts = get_quick_prompts_data()
        return JSONResponse(content=prompts)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading quick prompts file.")

# Endpoint to ask the LLM for creative ideas based on the positive prompt
@router.post("/ask_llm/")
async def ask_llm(request: LLMRequest):
    try:
        response = ask_llm_service(request.positive_prompt)
        return JSONResponse(content={"assistant_reply": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interacting with LLM: " + str(e))

# Endpoint to generate images
@router.post("/generate_images/")
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

        return image_responses[0]  # Return the first image for simplicity
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")
