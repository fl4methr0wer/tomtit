from uuid import uuid4
class Card:
    def __init__(self, title, content):
        self.id = str("card-"+str(uuid4()))
        self.title = title
        self.content = content

    def __str__(self):
        return f"Card:\n\tid:{self.id};\n\ttitle:{self.title};\n\tcontent:{self.content}"