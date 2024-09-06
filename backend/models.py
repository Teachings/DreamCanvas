from pydantic import BaseModel

# Request model for LLM
class LLMRequest(BaseModel):
    positive_prompt: str

# Request model for image generation
class PromptRequest(BaseModel):
    positive_prompt: str
    negative_prompt: str
    steps: int = 25
    width: int = 512
    height: int = 512
