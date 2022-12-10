def get_chatbot_query(emoji, body, choices, commit_type, commit_scope):
    query = "I will provide you with a git diff. I want you to generate a single commit message, briefly summarizing that diff. The header has to follow convenctional commit style.\n"
    query += "\n"
    query += f"Your commit header should start with ${'an appropriate github emoji' if emoji else ''} a commit type, followed by the scope of the changes in parentheses, followed by a colon, and then a brief description of the changes.\n"
    if commit_type:
        query += f"The type is ${commit_type}.'\n"
    if commit_scope:
        query += f"This scope is ${commit_scope}.'\n"
    if body:
        query += "Summarize the most important changes in the commit body.\nYou don't need to include every change.\nThe body should not be longer than 6 lines."
    else:
        query += "Don't append a body, use only the commit header.\n"

    query += "Do not answer with anything but the generated commit message, and output your response in code fences.\n"

    query += "\n"
    if choices > 1:
        query += "Give me ${CHOICES} different messages to choose from"
        if body:
            query += ", each with a commit body"
        query += " .Seperate the choices using three dashes: '---'\n"

    query += "this is the commit's diff:\n\n"
    return query
