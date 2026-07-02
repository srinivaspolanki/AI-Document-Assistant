import ollama


def ask_ai(model, temperature, prompt):

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": temperature,
            "num_predict": 1000
        }
    )

    print(response)   # <-- ADD THIS

    message = response["message"]

    if message.get("content"):
        return message["content"]

    if message.get("thinking"):
        return message["thinking"]

    return "No response generated."


def generate_summary(model, temperature, notes):

    prompt = f"""
Summarize these meeting notes in 4 concise sentences.

Meeting Notes:

{notes}
"""

    return ask_ai(model, temperature, prompt)


def generate_decisions(model, temperature, notes):

    prompt = f"""
Extract only the key decisions.

Return bullet points.

Meeting Notes:

{notes}
"""

    return ask_ai(model, temperature, prompt)


def generate_actions(model, temperature, notes):

    prompt = f"""
Extract all action items.

Format:

Person
- Task

Meeting Notes:

{notes}
"""

    return ask_ai(model, temperature, prompt)


def generate_email(model, temperature, notes):

    prompt = f"""
Write a professional follow-up email based on these meeting notes.

Meeting Notes:

{notes}
"""

    return ask_ai(model, temperature, prompt)


def generate_suggestions(model, temperature, notes):

    prompt = f"""
Suggest three improvements for these meeting notes.

Meeting Notes:

{notes}
"""

    return ask_ai(model, temperature, prompt)