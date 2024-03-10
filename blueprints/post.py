from flask import Blueprint, render_template, make_response, request
from domain.card import Card
import uuid, time

blueprint = Blueprint("post", __name__, url_prefix="/post")

CARDS = []
def deleteCardById(id):
    for card in CARDS:
        if lambda card: card.id == id:
            CARDS.remove(card)
@blueprint.route('/', methods=['POST'])
def create_card():
    card_id = "card-" + str(uuid.uuid4())
    title = request.form['title']
    content = request.form['content']
    print(f"ON POST CARD CONTENT:\n{content}")
    CARDS.append(Card(card_id, title, content))
    return render_template("htmx/post/post.html",
                           id = card_id, title=title, content=content)

@blueprint.route("/<id>", methods=["DELETE"])
def delete_card(id):
    time.sleep(1)
    deleteCardById(id)
    return make_response("", 200)