"""
agent.py

Defines the review_agent for reviewing tailored resumes.
"""

import logging
from google.adk.agents import Agent

from config import *
from .tools import increment_iteration_counter, update_current_score

# Create the review agent
review_agent = Agent(
    name="review_agent",
    model=LLM_MODEL,
    description="An agent that reviews the tailored resume written by the tailoring_agent and provides feedback and score.",
    instruction='''
    You are an expert recruiter and hiring manager with experience in evaluating resumes. Following are the tailored resume and job description.

    **INPUTS**:
    TAILORED RESUME:
    {tailoredResume}\n\n
    --------------------------------\n\n
    JOB DESCRIPTION:
    {jobDescription}\n\n
    --------------------------------

    Your tasks:

    1. Score tailored resume (0-100) based on overall alignment with the JD. Take into account multiple dimensions such as:
        - Skills & Tools match
        - Relevant experience & achievements
        - Domain/industry alignment
        - Education & certifications
        - Clarity, structure, and presentation
        - Business impact demonstrated

    2. Suggest scope for improvement, including:
        - Missing or weak skills compared to JD
        - Gaps in role expectations vs. my experience
        - Resume formatting/phrasing improvements
        - How to make achievements more quantifiable and impactful

    3. Update the score and feedback in the state using the "update_current_score" tool.

    4. Use the tool "increment_iteration_counter" to increment the iteration counter in the session state each time you provide feedback.

    **OUTPTUT**:
    Once completed all the steps, provide an update to the manager that you have successfully updated the score and feedback in the state.
    ''',
    tools=[increment_iteration_counter, update_current_score]
)
