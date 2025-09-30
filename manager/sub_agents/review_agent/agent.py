from google.adk.agents import Agent

review_agent = Agent(
    name="review_agent",
    model="gemini-2.0-flash",
    description="An agent that reviews the tailored resume written by the tailoring_agent and provides feedback and score.",
    instruction='''
    You are an agent that reviews the tailored resume and provides feedback and a score out of 100 like a professional ATS.
    Your task is to evaluate the tailored resume based on its relevance to the job description and the effectiveness of the key skills, experiences, and keywords highlighted.

    The inputs to the "review_agent" tool are as follows:
    {
        tailored_resume: "The tailored resume"
    }

    Your output should be a JSON object with the following structure:
    {
        feedback: "Your feedback on the tailored resume",
        score: "Relevance score out of 100"
    }
    '''
)
