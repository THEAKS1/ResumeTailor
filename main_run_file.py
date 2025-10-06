"""
main_run_file.py

Main entry point for running the ResumeTailor manager agent.
"""

from uuid import uuid4
from dotenv import load_dotenv

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.genai.errors import ServerError

from config import *
from manager.agent import manager_agent
from utils.retryDecorator import retry_on_server_error

load_dotenv()

@retry_on_server_error
async def run_manager_with_retry(runner, user_id, session_id, new_message):
    """
    This function wraps the runner.run() logic so the decorator can be applied.
    """
    # Run the agent and return the final response
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                return str(event.content.parts[0].text)
    return "The agent finished its run without providing a final response."

async def agent_call_start(resume, jd, USER_ID):
    # Setup session state for the agent
    session_service = InMemorySessionService()
    initial_state = {
        "userId": USER_ID,
        "resume": f"{resume}",
        "jobDescription": f"{jd}",
        "tailoredResume": "",
        "iterationCounter": 1,
        "currentScore": 0,
        "reviewFeedback": "",
        "keySkills": [],
        "experiences": [],
        "keywords": [],
        "maxIterations": MAX_ITERATIONS,
        "scoreThreshold": SCORE_THRESHOLD
    }

    SESSION_ID = str(uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state

    )

    runner = Runner(
        agent=manager_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    new_message = types.Content(
        role="user", parts=[types.Part(text=f"""Here is my resume and job description. Tailor my resume accordingly.""")]
    )

    try:
        out = await run_manager_with_retry(runner, USER_ID, SESSION_ID, new_message)
        print("Manager agent finished successfully.")
        return out
    except ServerError:
        print(f"Error: Final attempt failed for manager agent after {MAX_RETRY_PER_AGENT} attempts.")
        return "I'm sorry, the AI service is currently overloaded. Please try again in a few moments."

