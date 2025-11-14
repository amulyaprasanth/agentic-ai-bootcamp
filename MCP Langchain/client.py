from typing import Any


from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq

import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    client = MultiServerMCPClient(
        { 
            "math": {
                "command": "python",
                "args": ["mathserver.py"], # ensure correct absolute path
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp", # ensure server is running here
                "transport": "streamable-http"
            }
        } 
    )
    
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
    
    tools = await client.get_tools()
    model = ChatGroq(model="openai/gpt-oss-20b")
    
    agent = create_agent(
        model=model, tools=tools
    )
    
    math_response = await agent.ainvoke({
        "messages": [("user", "what is 2 + (5 * 6)")]
    })
    
    weather_response: Any = await agent.ainvoke(
        {"messages": [("user", "What is the weather in Hyderabad")]}
    )
    
    print("Math response: ", math_response['messages'][-1].content)
    print("Weather response: ", weather_response['messages'][-1].content)
    
    
if __name__ == "__main__":
    asyncio.run(main())