import anthropic
import os

anthropic_client = anthropic.Anthropic(api_key="INSERT API HERE LATER")

def get_claude_layman(paper_text, query_prompt, layman_prompt):
    message = anthropic_client.messages.create(
        model=os.getenv("CLAUDE_MODEL"),
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": f"{layman_prompt}\n{query_prompt}\n\nPaper:\n{paper_text}"}],
        )
    return message.content[0].text.strip()
