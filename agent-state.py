from dotenv import load_dotenv

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context, JsonSerializer
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from llama_index.llms.google_genai import GoogleGenAI

import os

load_dotenv()

MODEL="gemini-2.5-flash" # @param ["gemini-3-pro-preview", "gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro"]
PROJECT_ID=os.getenv("GCP_PROJECT_ID")
LOCATION=os.getenv("GCP_LOCATION")

llm = GoogleGenAI(
    model=MODEL,
    vertexai_config={"project": PROJECT_ID, "location": LOCATION},
)

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

finance_tools = YahooFinanceToolSpec().to_tool_list()
finance_tools.extend([multiply, add])

workflow = AgentWorkflow.from_tools_or_functions(
    finance_tools,
    llm=llm,
    system_prompt="You are an agent that can perform basic mathematical operations using tools."
)

# configure a context to work with our workflow
ctx = Context(workflow)

async def main():
    print("User: Hi, my name is Laurie!")
    response = await workflow.run(user_msg="Hi, my name is Laurie!",ctx=ctx)
    print(f"Agent: {response}")

    print("User: What's my name?")
    response2 = await workflow.run(user_msg="What's my name?")
    print(f"Agent: {response2}")

    # convert our Context to a dictionary object
    #ctx_dict = ctx.to_dict(serializer=JsonSerializer())

    # create a new Context from the dictionary
    #restored_ctx = Context.from_dict(
    #    workflow, ctx_dict, serializer=JsonSerializer()
    #)

    print("User: What's my name? (with restored context)")
    response3 = await workflow.run(user_msg="What's my name?",ctx=ctx)
    print(f"Agent: {response3}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())