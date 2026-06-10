import os
import certifi
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
import requests

from langchain.agents import create_react_agent, AgentExecutor

# os.environ["SSL_CERT_FILE"] = certifi.where()
loaded = load_dotenv()
print("Loaded:", loaded)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHER_STACK_API")

search_tool = TavilySearchResults(max_results=2)

# Custom Tool Function

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a given city using WeatherStack API.
    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"
    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']} degree Celcius\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

result = search_tool.invoke("Give me the latest news on AI")
# print(result)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9, openai_api_key=OPENAI_API_KEY)

# Prompt

prompt = hub.pull("hwchase17/react")
print(prompt)

# Tools

tools = [search_tool, get_weather_data]

# Create the ReAct agent

agent = create_react_agent(llm = llm, tools = tools, prompt = prompt)

# Agent Executor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent with a query

response = agent_executor.invoke({
    "input": (
        "What is the capital of India and what is its current weather?"
    )
})

print(response["output"])