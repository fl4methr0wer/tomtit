from flask import Blueprint, render_template, make_response, request
from domain.Card import Card
import uuid, time

blueprint = Blueprint("post", __name__, url_prefix="/card")

CARDS = []
def deleteCardById(id):
    global CARDS  # Use the global keyword to modify the global variable
    # Filter out cards with the specified id using a list comprehension
    CARDS = [card for card in CARDS if card.id != id]

@blueprint.route("/", methods=["GET"])
def get_all_cards():
    return render_template("htmx/card/card_list.html", cards = CARDS)
@blueprint.route('/', methods=['POST'])
def create_card():
    title = request.form['title']
    content = request.form['content']
    newCard = Card(title, content)
    CARDS.insert(0, newCard)
    return render_template("htmx/card/card.html",
                           card=newCard)

@blueprint.route("/<id>", methods=["DELETE"])
def delete_card(id):
    time.sleep(1) # just to show the spinner
    deleteCardById(id)
    return make_response("", 200)