from uuid import uuid4
class Card:
    def __init__(self, title, content):
        self.id = str("card-"+str(uuid4()))
        self.title = title
        self.content = content

    def __str__(self) -> str:
        str_repr = "Card("
        str_repr += f"id:{self.id}"
        str_repr += f", title:{self.title}"
        str_repr += f", content:{self.content}"
        str_repr += ")"
        return str_repr