from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.analysis_agent.agent import analysis_agent
from .sub_agents.tailoring_agent.agent import tailoring_agent
from .sub_agents.review_agent.agent import review_agent
from config import *

manager_agent = Agent(
    name="manager",
    model=LLM_MODEL,
    description="An agent that manages resume tailoring tasks.",
    instruction='''
    You are a manager responsible for delegating resume tailoring tasks. Your goal is to achieve a review score of 90 or higher, but you must stop after a maximum of 3 attempts to avoid getting stuck.
    You will receive requests from users regarding their resume and job description.

    Here is your workflow:
    1.  **Initialize**: Set an attempt counter to 1. The maximum number of attempts is 3.

    2.  **First Attempt (Attempt 1)**:
        a.  Analyze the user's resume and job description using the "analyzer" tool.
        b.  Tailor the resume using the "tailor" tool based on the analysis.
        c.  Review the tailored resume using the "reviewer" tool to get a score and feedback.

    3.  **Iteration Loop (Up to 3 Attempts Total)**:
        a.  Check the score from the reviewer.
        b.  **If the score is 90 or above**, the process is complete. Proceed to Step 4.
        c.  **If the score is below 90 AND your attempt counter is less than 3**:
            i.  Increment the attempt counter.
            ii. Repeat only the two process (Tailor and Review), but this time, provide the feedback from the previous review to the "analyzer" and "tailor" agents so they can improve.
        d.  **If the score is below 90 AND your attempt counter has reached 3**:
            i.  Stop the process. The loop is finished.
            ii. Proceed to Step 4 with the best resume you have created so far.

    4.  **Finalize and Report**:
        a.  Compare the final tailored resume (the one with the highest score) with the original resume and provide a summary of the changes.
        b.  If the final score is still below 90, inform the user that you've made the best possible improvements within 3 attempts and present the result.
        c.  If no changes were made at all, inform the user that their resume is already well-suited for the job.

    The inputs to the different tools are as follows:
    - For "analysis_agent" tool:
        {
            resume: "User's resume",
            job_description: "Job description provided by the user",
            feedback: "Feedback from the review_agent (if any)"
        }
    - For "tailoring_agent" tool:
        {
            resume: "User's resume",
            key_skills: ["skill1", "skill2"],
            experiences: ["experience1", "experience2"],
            keywords: ["keyword1", "keyword2"],
            feedback: "Feedback from the review_agent (if any)"
        }
    - For "review_agent" tool:
        {
            tailored_resume: "The tailored resume",
            job_description: "Job description provided by the user",
        }
    ''',
    tools=[AgentTool(analysis_agent), AgentTool(tailoring_agent), AgentTool(review_agent)]
)
