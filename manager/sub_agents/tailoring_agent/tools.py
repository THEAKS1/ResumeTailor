from google.adk.tools import ToolContext

def update_tailored_resume(tailored_resume: str, tool_context: ToolContext):
    """
    A tool to update the tailored resume in the session state.
    """
    tool_context.state["tailoredResume"] = tailored_resume
    return {
        "action": "update_tailored_resume",
        "message": f"Tailored resume updated in state. New value: {tool_context.state['tailoredResume']}",
    }