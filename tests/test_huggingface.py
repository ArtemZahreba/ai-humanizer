
from services.huggingface_service import HuggingFaceService


hf_service = HuggingFaceService()

result = hf_service.generate_text(
    model_id="meta-llama/Llama-3.1-8B-Instruct:novita",
    prompt="What is the capital of France?",
    max_tokens=100
)

print("Model response:")
print(result)
