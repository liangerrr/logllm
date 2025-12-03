import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# ✅这是服务器上的绝对路径
model_path = "/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B"

print(f"Testing model path: {model_path}")

if not os.path.exists(model_path):
    print("❌ Error: Path does not exist on this machine!")
else:
    print("✅ Path exists. Loading model...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        print("✅ SUCCESS! Model loaded to GPU.")

        # 简单的推理测试
        input_text = "Log analysis is"
        inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=10)
        print("Output:", tokenizer.decode(outputs[0]))

    except Exception as e:
        print(f"❌ Failed: {e}")