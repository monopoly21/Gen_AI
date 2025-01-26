from crewai import Task
from tools import tool
from agents import blog_researcher,blog_writer
from tools import yttool



research_task=Task(
    description=(
        "Identify the video {topic}",
        "Get detailed information about the video from the youtube channel",
    ),
    expected_output='A comprehensive 3 paragraphs long report based on the {topic} of the video content',
    tools=[yttool],
    agent=blog_researcher
)

writing_task=Task(
    description=(
        "Get the info from the youtube channel on the topic {topic}",
    ),
    expected_output='Summarize the info from the youtube channel video on the topic {topic} and create the content for the blog',
    tools=[yttool],
    agent=blog_writer,
    async_execution=False,
    output_file='blog_content.md'
)


