from google.adk.tools import ToolContext

def update_extracted_info(key_skills: list[str], experiences: list[str], keywords: list[str], tool_context: ToolContext) -> dict:
    """
    A tool to update the extracted information in the session state.
    """
    state = tool_context.state
    state['keySkills'] = key_skills
    state['experiences'] = experiences
    state['keywords'] = keywords
    return {
        "action": "update_extracted_info",
        "message": "Extracted information updated successfully.\n"
        "Key Skills: " + ", ".join(state['keySkills']) + 
        "\nExperiences: " + ", ".join(state['experiences']) + 
        "\nKeywords: " + ", ".join(state['keywords'])
    }