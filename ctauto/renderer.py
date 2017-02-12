def render(blocks, name):
    with open(name, "wb") as f:
        for block in blocks:
            f.write(block.content)
