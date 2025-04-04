from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small")

def summarize_text(text: str) -> str:
    prompt = "summarize: " + text
    summary = summarizer(prompt, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
