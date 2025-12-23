# Module 08 - AI Agents with Agno

This module demonstrates building AI agents using the Agno framework with local LLMs via Ollama.

## Prerequisites

### 1. Start Ollama

Before running any examples, you need to have Ollama running. If you haven't installed Ollama yet, see the detailed instructions in [module-04/README.md](../module-04/README.md#installing-ollama).

```bash
ollama serve
```

### 2. Pull the Required Model

The examples use the `granite4:micro-h` model. Download it before running:

```bash
ollama pull granite4:micro-h
```

### 3. Verify Ollama is Running

```bash
ollama list
```

You should see `granite4:micro-h` in the list of available models.

## Understanding Agents vs. Direct LLM Queries

Before running the agent examples, let's see the difference between querying an LLM directly and using an agent framework.

### Direct LLM Query (CLI)

Try asking the same question that the agent will handle, but directly to Ollama:

```bash
ollama run granite4:micro-h "What is the stock price of NVIDIA?"
```

**What happens:** The LLM will respond based on its training data, but it cannot access real-time information or use external tools. It may give you outdated information or say it doesn't have access to current stock prices.

**Why this matters:** This demonstrates the limitation of using an LLM alone - it's a language model that can only work with its training data, not interact with the real world.

### Agent Query (Python)

Now compare this to running `01_basic_agent.py`, which uses the same model but with agent capabilities:

```bash
python 01_basic_agent.py
```

**What happens:** The agent can use tools (YFinance in this case) to fetch real-time stock data, process it, and provide an accurate answer.

**The difference:** Agents can use tools, access APIs, perform actions, and reason about when to use them - making them capable of interacting with the real world, not just generating text based on training data.

## Running the Examples

Once Ollama is running, you can execute the examples:

```bash
python 01_basic_agent.py
python 02_hacker_news_agent.py
```

### OpenAI API Key (for 03_youtube_agent.py)

The YouTube agent example uses OpenAI's API instead of local Ollama. Create a `.env` file in the workspace root directory (`practical-ai-for-se/.env`):

```
OPENAI_API_KEY=your-api-key-here
```

Then run:
```bash
python 03_youtube_agent.py
```

### RAG Example (04_simple_rag.py)

The RAG example requires additional dependencies and PostgreSQL with pgvector:

```bash
pip install unstructured markdown
```

Start the PostgreSQL database with pgvector:
```bash
cd module-08/docker
docker compose up -d
```

Then run:
```bash
python 04_simple_rag.py
```

## Troubleshooting

**ConnectionError: Failed to connect to Ollama**

This error means Ollama is not running. Start it with `ollama serve` in a separate terminal.

**Model not found**

Run `ollama pull granite4:micro-h` to download the model first.

