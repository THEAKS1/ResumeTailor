from google.adk.agents import Agent

from config import *
from .tools import update_extracted_info

analysis_agent = Agent(
    name="analysis_agent",
    model=LLM_MODEL,
    description="An agent that analyzes resumes and job descriptions and finds key skills, experiences and keywords.",
    instruction='''
    You are an agent that analyzes resumes and job descriptions to identify key skills, experiences, and keywords.
    Your task is to extract relevant information from the user's resume and the job description provided.
    Additionally, you may get a feedback from the review_agent to improve your analysis. This feedback should be considered in your analysis.

    **INPUTS**:
    RESUME:
    {resume}\n\n
    --------------------------------\n\n
    JOB DESCRIPTION:
    {jobDescription}\n\n
    --------------------------------

    Note: All the extracted entities should be a valid python list of strings.
    Update the extracted information to the session state using the "update_extracted_info" tool.
    ''',
    tools=[update_extracted_info]
)