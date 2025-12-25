# Small helpers. Replace count_tokens with a real tokenizer for production.
def count_tokens(text: str) -> int:
    # crude estimate: 1 token ≈ 4 chars (use tiktoken for precise counts)
    return max(1, len(text) // 4)

def summarize_text_naive(text: str, max_chars: int) -> str:
    # placeholder summarizer: trim preserving start+end with marker
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    return text[:half] + "\n\n[...] TRUNCATED [...] \n\n" + text[-half:]

def make_context_block(doc: dict, idx: int) -> str:
    """
    doc expected keys: id, text, meta (with optional file/page), score
    Returns a human-friendly context block.
    """
    src = doc.get("meta", {}).get("file", doc.get("id", "unknown"))
    page = doc.get("meta", {}).get("page", "NA")
    header = f"Context ({idx}) — source: {src}, page: {page}, score: {doc.get('score', None)}"
    sep = "\n" + ("-" * 60) + "\n"
    return f"{header}\n{sep}{doc.get('text','')}\n{sep}"


#COMPLETE CODE FROM CAHTGPT. NEED TO REVIEW THIS ONCE. DONT USE ANYWHERE 