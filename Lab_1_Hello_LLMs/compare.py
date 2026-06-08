"""
compare.py — Send the same prompt to both Ollama and OpenAI,
print responses side-by-side. Demonstrates LangChain's provider abstraction.
"""
import time
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

PROMPT = "In one sentence, explain why BGP uses TCP instead of UDP."


def ask(llm):
    """Stream the response chunk-by-chunk, return (full_text, elapsed_seconds)."""
    start = time.time()
    chunks = []
    for chunk in llm.stream([HumanMessage(content=PROMPT)]):
        print(chunk.content, end="", flush=True)   # print each chunk as it arrives
        chunks.append(chunk.content)
    print()                                         # newline once the stream ends
    elapsed = time.time() - start
    return "".join(chunks), elapsed


# Same interface, different providers
ollama = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
openai = ChatOpenAI(model="gpt-4o-mini", temperature=0)

print(f"Prompt: {PROMPT}\n")

for llm, label in [(ollama, "Ollama / llama3.2:3b"),
                   (openai, "OpenAI / gpt-4o-mini")]:
    text, elapsed = ask(llm)
    print(f"=== {label} ({elapsed:.2f}s) ===")
    print(text)
    print()
