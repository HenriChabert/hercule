class Sentinel:
    """A unique marker object to indicate a special condition."""
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Sentinel: {self.name}>"

# Define a reusable sentinel object
NOT_PROVIDED = Sentinel("NOT_PROVIDED")