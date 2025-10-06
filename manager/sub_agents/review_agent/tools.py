"""
tools.py

Tool functions for the review_agent.
"""

from google.adk.tools import ToolContext

def increment_iteration_counter(tool_context: ToolContext):
    '''Tool to increment the iteration counter in the session state.'''
    # Increment the iteration counter
    tool_context.state["iterationCounter"] += 1

    return {
        "action": "increment_iteration_counter",
        "message": f"Iteration counter incremented to {tool_context.state['iterationCounter']}"
    }

def update_current_score(score: int, feedback: str, tool_context: ToolContext):
    '''
    Tool to update the current score and feedback in the session state.
    '''
    # Update score and feedback in session state
    tool_context.state["currentScore"] = score
    tool_context.state["reviewFeedback"] = feedback
    return {
        "action": "update_current_score",
        "message": f"Current score updated to {tool_context.state['currentScore']} and feedback to '{tool_context.state['reviewFeedback']}'"
    }