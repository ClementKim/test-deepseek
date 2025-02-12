from transformers import pipeline

messages = [
    {"role": "user",
    "content": "Who are you?"}
]

pipe = pipeline("text-generation", model = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B")
pipe(messages)

