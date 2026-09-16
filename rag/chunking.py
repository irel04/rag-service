
# Split texts into overlapping chunks
def split_text(text: str, chunk_size=1000, chunk_overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        # step forward but overlap a little to keep context
        start = end - chunk_overlap
    return chunks