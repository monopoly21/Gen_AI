from crewai import Agent
from tools import yttool


# Create a senior blog content researcher

llm=

blog_researcher = Agent(
    role="Blog Resarcher from Youtube Videos",
    goal='get the relevant video content for the topic {topic} from yt Channel',
    verbose=True,
    memory=True,
    backstory=("Expert in finding the relevant content from youtube videos"),
    tools=[],
    allow_delegation=True,
    llm=llm,
)

# Create a senior blog content writer Agent

blog_writer = Agent(
    role="Narrate the compelling tech stories about the video {topic}",
    goal='get the relevant video content for the topic {topic} from yt Channel',
    verbose=True,
    memory=True,
    backstory=("With a flair for simplifying complex topics,you craft",
               "engaging stories that resonate with the audience"),
    tools=[yttool],
    llm=llm,
    allow_delegation=False,
)

