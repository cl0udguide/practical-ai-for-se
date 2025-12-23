# Import the core Agent class from Agno framework
from agno.agent import Agent
# Import Ollama model wrapper for running local LLMs
from agno.models.ollama import Ollama
# Import Hacker News tools for fetching posts and stories
from agno.tools.hackernews import HackerNewsTools
# Import datetime for timestamping the report
from datetime import datetime
import os

# Create an Agent instance configured as a security researcher
# - model: Local Ollama model (granite4:micro-h)
# - instructions: System prompt defining agent as security research specialist
# - markdown: Enable markdown formatting for better report output
# - tools: HackerNews toolkit for fetching and searching posts
# - debug_mode: Uncomment to see reasoning and tool calls
agent = Agent(
    model=Ollama(id="granite4:micro-h"),
    instructions="You are a security research agent. Research the latest security vulnerabilities and exploits from Hacker News over the past 30 days. Provide a concise summary of the most important security-related posts.",
    markdown=True,
    tools=[HackerNewsTools()],
#    debug_mode=True,
)

# Define the research prompt focusing on security topics
prompt = "Research and summarize the most important security vulnerabilities, exploits, and cybersecurity news from Hacker News in the last 30 days. Focus on critical CVEs, zero-day exploits, and significant security incidents."

print("Researching Hacker News for security vulnerabilities...")
# Run the agent - it will use HackerNews tools to fetch and analyze posts
response = agent.run(prompt)

# Save report to markdown file with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
filename = f"security_report_{timestamp}.md"

# Write the report with a header and the agent's response
with open(filename, 'w', encoding='utf-8') as f:
    f.write(f"# Security Vulnerabilities Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(response.content)

print(f"\nReport saved to: {filename}")
print("\n" + "="*80)
# Print the report content to console
print(response.content)
