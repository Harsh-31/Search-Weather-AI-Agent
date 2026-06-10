# LangChain Single Agent

A minimal LangChain demo showing a ReAct-style agent that uses modern tools to answer user queries.

This repository includes:

- `main.py` — a script that loads OpenAI, Tavily, and WeatherStack integrations and runs a simple ReAct agent.
- `app.py` — a Streamlit front-end for a weather-focused AI assistant with a clean dark/light theme.
- `requirements.txt` — Python package dependencies for the project.
- `research/agent_demo.ipynb` — research notebook for experimentation.

## Features

- ReAct agent built with `langchain` and `langchain-openai`
- Search integration using `langchain-community` Tavily tool
- Weather lookup via a custom `get_weather_data` tool calling the WeatherStack API
- Streamlit UI for interactive weather queries

## Requirements

- Python 3.11+ (or compatible Python 3.x)
- OpenAI API key
- Tavily API key
- WeatherStack API key

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the repository root with the required API keys:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHER_STACK_API=your_weatherstack_api_key
```

## Running the agent script

To run the ReAct agent example in `main.py`:

```bash
python main.py
```

This script:

- loads environment variables
- initializes the OpenAI chat LLM
- defines a custom weather tool
- creates a ReAct agent with search and weather tools
- runs a sample query

## Running the Streamlit app

To start the Streamlit interface in `app.py`:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (typically `http://localhost:8501`).

## Configuration

- `OPENAI_API_KEY` — required for OpenAI access
- `TAVILY_API_KEY` — required for Tavily search tool
- `WEATHER_STACK_API` — required for WeatherStack weather lookups

## Notes

- The example agent is configured for exploration and demonstration, not production use.
- The Streamlit app is styled with a custom theme and supports dark/light mode toggling.
- If API calls fail, verify your keys and network connectivity.

## License

This repository does not include an explicit license.