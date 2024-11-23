def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    return [split_block.strip() for split_block in split_blocks if split_block != ""]
