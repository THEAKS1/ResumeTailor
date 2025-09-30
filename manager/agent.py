from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.analysis_agent.agent import analysis_agent
from .sub_agents.tailoring_agent.agent import tailoring_agent
from .sub_agents.review_agent.agent import review_agent

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="An agent that manages resume tailoring tasks.",
    instruction='''
    You are a manager that is responsible for delegating resume tailoring tasks to specialized agents.
    You will receive requests from users regarding their resume and job description.

    A resume tailoring task involves the following steps:
    1. Analyze the user's resume and the job description to identify the key skills, experiences and keywords required for the job using "analysis_agent" tool.
    2. Tailor the user's resume to highlight the relevant skills, experiences and keywords using "tailoring_agent" tool.
    3. Review the tailored resume and provide a feedback and a score out of 100 using "review_agent" tool.
    4. If the score is less than 90, iterate the tailoring process until the score is 90 or above.
    5. Once the score is 90 or above, provide the final tailored resume to the user.
    6. Compare the final tailored resume with the original resume and provide a summary of the changes made. If no changes were made, inform the user that their resume is already well-suited for the job description.

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
            tailored_resume: "The tailored resume"
        }
    ''',
    tools=[AgentTool(analysis_agent), AgentTool(tailoring_agent), AgentTool(review_agent)]
)