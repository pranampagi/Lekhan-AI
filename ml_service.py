from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Manual loading of model and tokenizer to bypass pipeline registry issues
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_summary(text: str) -> str:
    """Generate a summary of the given text using the BART model.

    Takes the input document text and returns a concise summary
    produced by the facebook/bart-large-cnn model.

    Args:
        text: The document text to summarize.

    Returns:
        A summarized version of the input text.
    """
    if not text or not text.strip():
        return ""

    # Encode the input text
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)

    # Generate summary IDs
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        max_length=150,
        min_length=40,
        early_stopping=True,
    )

    # Decode the summary
    summary = tokenizer.decode(
        summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    return summary
