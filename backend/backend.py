from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
#from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b")

class Chatstate(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

def chat(state:Chatstate):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages':[response]}

##create sqlite checkpointer
conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(Chatstate)
graph.add_node("chat",chat)
graph.add_edge(START, "chat")
graph.add_edge("chat",END)

chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
