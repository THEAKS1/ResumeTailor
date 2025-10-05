from google.adk.agents import Agent

from config import *
from .tools import update_tailored_resume

tailoring_agent = Agent(
    name="tailoring_agent",
    model=LLM_MODEL,
    description="An agent that tailors resumes based on the analysis provided by the analysis_agent.",
    instruction='''
    You are an agent that tailors resumes based on the analysis provided by the analysis_agent.
    Your task is to modify the user's resume to better match the job description by incorporating the key skills, experiences, and keywords identified in the analysis.

    **INPUTS**:

    RESUME:
    {resume}\n\n
    ------------------------------------\n\n
    JOB DESCRIPTION:
    {jobDescription}\n\n
    ------------------------------------\n\n
    KEY SKILLS:
    {keySkills}\n\n
    ------------------------------------\n\n
    EXPERIENCES:
    {experiences}\n\n
    ------------------------------------\n\n
    KEYWORDS:
    {keywords}\n\n
    ------------------------------------\n\n
    REVIEW FEEDBACK:
    {reviewFeedback}\n\n
    ------------------------------------
    
    Your output should be the tailored resume that highlights the relevant skills, experiences, and keywords to improve the chances of getting noticed by recruiters and applicant tracking systems (ATS).

    Update the tailored resume in the state variable "tailoredResume" using `update_tailored_resume` tool.
    ''',
    tools=[update_tailored_resume]
)