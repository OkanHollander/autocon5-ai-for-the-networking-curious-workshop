"""hello_ollama.py — first call to the local LLM via Python."""
from ollama import Client

client = Client(host="http://localhost:11434")

response = client.chat(
    model="llama3.2:3b",
    messages=[
        {"role": "user", "content": "Explain OSPF in one sentence."}
    ],
)

print(response["message"]["content"])