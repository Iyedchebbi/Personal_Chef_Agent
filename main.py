from importlib.resources import path
from ast import Dict
from typing import Any
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
from prompt import SYSTEM_CHEF_PROMPT, CHEF_PROMPT
from tools import web_search
from photo_decoder import choose_image_file,build_image_message
import logging 

logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s",
)

load_dotenv()


logging.info("Creating our agent ... ")

model = ChatOpenRouter(
    model = "nvidia/nemotron-3.5-super-vl:free",
    temperature=1.0
)


agent = create_agent(model = model,system_prompt =SYSTEM_CHEF_PROMPT,tools=[web_search])

logging.info("Choosing Our Image... ")


path = choose_image_file()
message =  build_image_message(path,CHEF_PROMPT)

logging.info("Invoking Our Agent... ")

response = agent.invoke({"messages" : [message]})
print(response["messages"][-1].content)