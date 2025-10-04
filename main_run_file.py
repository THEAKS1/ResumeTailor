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
    # initial_state = {
    #     "userId": USER_ID,
    #     "resume": "{resume}",
    #     "jobDescription": "{jobDescription}",
    #     "tailoredResume": ""
    # }

    SESSION_ID = str(uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=manager_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    new_message = types.Content(
        role="user",parts=[types.Part(text="""
                                      Resume: {resume}
                                      -----------------------
                                      Job Description: {jobDescription}
                                      """.format(resume=resume, jobDescription=jd))]
    )

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                out = str(event.content.parts[0].text)
                print(out)
                return out
