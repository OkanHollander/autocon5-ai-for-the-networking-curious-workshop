"""chat_app.py — chat UI backed by the Lab 3 network agent."""
import sys
from pathlib import Path
import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Import the BGP tool from Lab 3. We add Lab 3's folder to the import path
# so this stays a single self-contained file.
LAB3_DIR = Path(__file__).parent.parent / "Lab_3_LangChain_Network_Agent"
sys.path.insert(0, str(LAB3_DIR))
from bgp_tool import get_bgp_state  # noqa: E402


@st.cache_resource
def build_agent():
    """Build the agent once and cache it across reruns.

    @st.cache_resource is the right pattern for "expensive things you build
    once" — DB connections, model handles, LangChain agents. Without caching,
    Streamlit would rebuild this on every single rerun (every keystroke).
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a network engineering assistant for a small containerlab "
         "topology with three nodes: r1, r2, r3. Use tools when the user asks "
         "about specific routers. For general concept questions, answer from "
         "your own knowledge without calling tools."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    tools = [get_bgp_state]
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


agent = build_agent()

# ---------- UI ----------

st.title("Network Co-Pilot")
st.caption("Ask questions about the lab topology (r1, r2, r3).")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask me about your network..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = agent.invoke({"input": prompt})
        st.write(result["output"])

    st.session_state.messages.append({"role": "assistant", "content": result["output"]})