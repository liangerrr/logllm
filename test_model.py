import os

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BertTokenizerFast,
    BertModel,
)


LLAMA_PATH = "/hy-tmp/model_weights/LLM-Research/Meta-Llama-3-8B"
BERT_PATH = "/hy-tmp/model_weights/AI-ModelScope/bert-base-uncased"


def test_llama():
    print(f"Testing Llama path: {LLAMA_PATH}")
    if not os.path.exists(LLAMA_PATH):
        print("❌ Error: Llama path does not exist on this machine!")
        return

    print("✅ Llama path exists. Loading model...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(LLAMA_PATH)
        model = AutoModelForCausalLM.from_pretrained(
            LLAMA_PATH,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        print("✅ SUCCESS! Llama model loaded to GPU.")

        # 简单的推理测试
        input_text = "Log analysis is"
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=10)
        print("Llama Output:", tokenizer.decode(outputs[0]))
    except Exception as e:
        print(f"❌ Llama test failed: {e}")


def test_bert():
    print(f"\nTesting BERT path: {BERT_PATH}")
    if not os.path.exists(BERT_PATH):
        print("❌ Error: BERT path does not exist on this machine!")
        return

    print("✅ BERT path exists. Loading model...")
    try:
        tokenizer = BertTokenizerFast.from_pretrained(BERT_PATH)
        model = BertModel.from_pretrained(BERT_PATH)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        # 简单的前向测试
        inputs = tokenizer(
            "This is a test sentence for BERT.",
            return_tensors="pt",
        ).to(device)
        outputs = model(**inputs)
        pooled = outputs.pooler_output
        print(f"✅ SUCCESS! BERT model loaded to {device}. Pooled shape: {pooled.shape}")
    except Exception as e:
        print(f"❌ BERT test failed: {e}")


if __name__ == "__main__":
    test_llama()
    test_bert()