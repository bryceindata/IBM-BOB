def build_prompt(mode, user_input, context=None):
    base_instructions = "You are IBM Bob, an AI engineering copilot."

    context_block = f"Context: {context}" if context else "No additional context"

    mode_instructions = {
        "repo": "Explain system architecture and dependencies clearly.",
        "incident": "Analyze logs, commits, and find root cause.",
        "workflow": "Convert request into automation scripts."
    }.get(mode, "General assistance")

    return f"""
{base_instructions}

Mode: {mode}
Task: {mode_instructions}

User Input:
{user_input}

{context_block}

Return structured, actionable output.
"""
