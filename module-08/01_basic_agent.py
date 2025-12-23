# Import the core Agent class from Agno framework
from agno.agent import Agent
# Import Ollama model wrapper for running local LLMs
from agno.models.ollama import Ollama
# Import YFinance tools for stock market data retrieval
from agno.tools.yfinance import YFinanceTools

# Create an Agent instance with:
# - model: Local Ollama model (granite4:micro-h)
# - instructions: System prompt defining agent behavior
# - markdown: Disable markdown formatting in responses
# - tools: YFinance toolkit for fetching stock prices and financial data
agent = Agent(
    model=Ollama(id="granite4:micro-h"),
    instructions="You are an agent focused on responding in one line. All your responses must be super concise and focused.",
    markdown=False,
    tools=[YFinanceTools()],
    debug_mode=True,
)

# Run the agent with a query - the agent will use YFinance tools to fetch NVIDIA stock price
runx = agent.run("What is the stock price of NVIDIA?")
# Print the agent's response content
print(runx.content)
