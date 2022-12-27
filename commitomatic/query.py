def get_gpt_codex_prompt(diff, header=None, commit_type=None):
    """Get the prompt for GPT-Codex."""
    git_diff = "git diff ."

    if header:
        commit_command = f"git commit -m <<EOF {header}\n"
    elif commit_type:
        commit_command = f"git commit -m <<EOF {commit_type}: "
    else:
        commit_command = "git commit -m <<EOF"
    prompt = f"git diff .\n{diff}\n\n{commit_command}"
    return prompt

def get_gpt_prompt(diff):
    """Get the prompt for GPT."""

    query = "# Write a commit message for the following diff. Use conventional commit style. Add bullet points in the body.\n"
    query += "# Start diff\n"
    query += diff
    query += "\n# End diff\n"
    return query
