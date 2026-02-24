from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Manual loading of model and tokenizer to bypass pipeline registry issues
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Maximum token length the BART model can handle per input
MAX_CHUNK_TOKENS = 1024


def chunk_text(text: str, max_tokens: int = MAX_CHUNK_TOKENS) -> list[str]:
    """Split text into chunks that fit within the model's token limit.

    Long documents exceed the 1024-token limit of BART, causing truncation
    or errors. This function splits the text into overlapping chunks so
    that each can be summarized independently.

    Args:
        text: The full document text.
        max_tokens: Maximum number of tokens per chunk.

    Returns:
        A list of text chunks, each within the token limit.
    """
    tokens = tokenizer.encode(text, add_special_tokens=False)

    if len(tokens) <= max_tokens:
        return [text]

    chunks = []
    # Use a stride of 80% to create slight overlap between chunks
    stride = int(max_tokens * 0.8)

    for i in range(0, len(tokens), stride):
        chunk_tokens = tokens[i : i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)

        # Stop if we've covered all tokens
        if i + max_tokens >= len(tokens):
            break

    return chunks


def generate_summary(text: str) -> str:
    """Generate a summary of the given text using the BART model.

    For documents exceeding the 1024-token limit, the text is split into
    chunks. Each chunk is summarized independently, and the chunk summaries
    are combined into a final summary.

    Args:
        text: The document text to summarize.

    Returns:
        A summarized version of the input text.
    """
    if not text or not text.strip():
        return ""

    chunks = chunk_text(text)

    # Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        inputs = tokenizer(
            [chunk], max_length=MAX_CHUNK_TOKENS, return_tensors="pt", truncation=True
        )

        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=150,
            min_length=40,
            early_stopping=True,
        )

        summary = tokenizer.decode(
            summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        chunk_summaries.append(summary)

    # If multiple chunks, combine and re-summarize
    if len(chunk_summaries) > 1:
        combined = " ".join(chunk_summaries)
        # Recursively summarize if the combined text is still too long
        return generate_summary(combined)

    return chunk_summaries[0]
