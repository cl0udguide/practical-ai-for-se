"""🎥 YouTube Agent - Your Video Content Expert!

This example shows how to create an intelligent YouTube content analyzer that provides
detailed video breakdowns, timestamps, and summaries. Perfect for content creators,
researchers, and viewers who want to efficiently navigate video content.

Example prompts to try:
- "Analyze this tech review: [video_url]"
- "Get timestamps for this coding tutorial: [video_url]"
- "Break down the key points of this lecture: [video_url]"
- "Summarize the main topics in this documentary: [video_url]"
- "Create a study guide from this educational video: [video_url]"
- "What are the main topics covered in [video_url]?"
- "Does this video [video_url] discuss [specific topic]? If so, when does it come up?"
- "What is the conclusion of this video: [video_url]?"
- "Are there any code examples in [video_url] and what do they demonstrate?"

Run: `pip install openai youtube_transcript_api agno python-dotenv` to install the dependencies
"""

# dedent removes leading whitespace from multi-line strings
from textwrap import dedent
# Load environment variables from .env file (for OPENAI_API_KEY)
from dotenv import load_dotenv

load_dotenv()

# Import the core Agent class from Agno framework
from agno.agent import Agent
# Import OpenAI model wrapper (this example uses OpenAI API, not local Ollama)
from agno.models.openai import OpenAIChat
# Import YouTube tools for fetching video transcripts and metadata
from agno.tools.youtube import YouTubeTools

# Create an Agent instance configured as a YouTube content analyst
# - name: Human-readable agent identifier
# - model: OpenAI GPT model (requires OPENAI_API_KEY in .env)
# - tools: YouTube toolkit for transcript extraction and video analysis
# - instructions: Detailed system prompt defining analysis methodology
youtube_agent = Agent(
    name="YouTube Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[YouTubeTools()],
    instructions=dedent("""\
        You are an expert YouTube content analyst with a keen eye for detail! 🎓
        
        Follow these steps for comprehensive video analysis:
        1. Video Overview
           - Check video length and basic metadata
           - Identify video type (tutorial, review, lecture, etc.)
           - Note the content structure
        2. Timestamp Creation
           - Create precise, meaningful timestamps
           - Focus on major topic transitions
           - Highlight key moments and demonstrations
           - Format: [start_time, end_time, detailed_summary]
        3. Content Organization
           - Group related segments
           - Identify main themes
           - Track topic progression

        Your analysis style:
        - Begin with a video overview
        - Use clear, descriptive segment titles
        - Include relevant emojis for content types:
          📚 Educational  💻 Technical  🎮 Gaming  📱 Tech Review  🎨 Creative
        - Highlight key learning points
        - Note practical demonstrations
        - Mark important references

        Quality Guidelines:
        - Verify timestamp accuracy
        - Avoid timestamp hallucination
        - Ensure comprehensive coverage
        - Maintain consistent detail level
        - Focus on valuable content markers
    """),
    # Include current date/time in context for time-aware responses
    add_datetime_to_context=True,
    # Enable markdown formatting for structured output
    markdown=True,
    # Uncomment to see reasoning and tool calls
    debug_mode=True,
)

# Run the agent with a video URL - uses print_response for streaming output
# The agent will fetch the transcript and analyze the video content
youtube_agent.print_response(
    "Analyze this video: https://www.youtube.com/watch?v=VHLYXuqja4c",
#    "Analyze this video: https://www.youtube.com/watch?v=RIshToi7-MQ",
    stream=True,
#    debug_mode=True,  # Uncomment to see reasoning and tool calls for this request
)

# More example prompts to explore:

# ============================================================================
# SPECIFIC QUESTION-BASED QUERIES (No need to watch the full video!)
# ============================================================================

# Ask targeted questions about video content:
"""
1. "What is the main tool used in this tutorial: [video_url]?"
2. "Does this video [video_url] explain authentication? If yes, where?"
3. "What problem does this video solve: [video_url]?"
4. "Are there any security best practices mentioned in [video_url]?"
5. "What version of Python does this tutorial use: [video_url]?"
6. "Does [video_url] discuss performance optimization? What are the key points?"
7. "What database is mentioned in this video: [video_url]?"
8. "Are there any prerequisites needed before watching [video_url]?"
"""

# ============================================================================
# DETAILED ANALYSIS TASKS
# ============================================================================

# Tutorial Analysis:
"""
1. "Break down this Python tutorial with focus on code examples: [video_url]"
2. "Create a learning path from this web development course: [video_url]"
3. "Extract all practical exercises from this programming guide: [video_url]"
4. "Identify key concepts and implementation examples: [video_url]"
"""

# Educational Content:
"""
1. "Create a study guide with timestamps for this math lecture: [video_url]"
2. "Extract main theories and examples from this science video: [video_url]"
3. "Break down this historical documentary into key events: [video_url]"
4. "Summarize the main arguments in this academic presentation: [video_url]"
"""

# Tech Reviews:
"""
1. "List all product features mentioned with timestamps: [video_url]"
2. "Compare pros and cons discussed in this review: [video_url]"
3. "Extract technical specifications and benchmarks: [video_url]"
4. "Identify key comparison points and conclusions: [video_url]"
"""

# Creative Content:
"""
1. "Break down the techniques shown in this art tutorial: [video_url]"
2. "Create a timeline of project steps in this DIY video: [video_url]"
3. "List all tools and materials mentioned with timestamps: [video_url]"
4. "Extract tips and tricks with their demonstrations: [video_url]"
"""
