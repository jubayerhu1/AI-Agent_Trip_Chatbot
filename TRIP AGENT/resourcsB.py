import os
import certifi
from dotenv import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from typing import TypedDict, Annotated
import operator
import uuid
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import(
                                        AnyMessage,
                                        HumanMessage,
                                        AIMessage,
                                        SystemMessage,
)

from langchain_groq import ChatGroq

# =========================
# LLM
# =========================

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file")

# =========================
# LLM
# =========================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY
)

# Test the llm does it work?
response = llm.invoke("hello what day is today")

print(response)