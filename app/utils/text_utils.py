import re

# Clean markdown-style LLM output
def clean_output(text: str) -> str:
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 - \2', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\n{2,}', '\n\n', text).strip()
    return text