from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from uuid import uuid4
import asyncio
from dotenv import load_dotenv

from config import *
from manager.agent import manager_agent

load_dotenv()

async def agent_call_start(resume, jd, USER_ID):
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
        role="user",parts=[types.Part(text=f"""Here is my resume and job description. Tailor my resume accordingly.""")]
    )

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                return str(event.content.parts[0].text)
