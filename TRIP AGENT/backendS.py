import os 
import certifi # path error solve the problem
from dotenv import load_dotenv
# keys loads 
load_dotenv()
# path errro solve the problem
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from typing import TypedDict, Annotated
import operator
# generate unique id
import uuid 
# Make agent to 
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
# Model of Groq
from langchain_groq import ChatGroq

from tools.flight_t1 import search_flights
#=============
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("key is missing .please add")

llm = ChatGroq(
    #model="llama-3.1-70b-versatile",
    model= "openai/gpt-oss-120b",
    api_key=GROQ_API_KEY)

response = llm.invoke("write a linked post about LLm Model setup not more then 100 words")
#print(response)
print(response.content)

#----------------------------
# State
#----------------------------

class TravelState(TypedDict):
    messages : Annotated[list[AnyMessage], operator.add]
    user_query : str
    flight_results : str
    hotel_results : str
    itinerary :str
    llm_calls :int


#------------------------------
# Flight 
#-----------------------------

def flight_agent(state : TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)

    return{
        "flight_results" : flight_data,
        "messages" :[
            AIMessage(content="Flisht results fetched.")
        ],
        "llm_calls" : state.get("llm_calls")
    }


#------------------------------
# Flight 
#-----------------------------





#------------------------------
# Flight 
#-----------------------------




#------------------------------
# Flight 
#-----------------------------