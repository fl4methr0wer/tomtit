from flask import Blueprint, render_template, make_response, request
from domain.Card import Card
import time

blueprint = Blueprint("cards", __name__, url_prefix="/cards")

CARDS = [
    Card("title 1", "content 1"),
    Card("title 2", "content 2"),
    Card("title 3", "content 3")
]
def deleteCardById(id):
    global CARDS  # Use the global keyword to modify the global variable
    # Filter out cards with the specified id using a list comprehension
    CARDS = [card for card in CARDS if card.id != id]

def reorderCardsByIdList(id_list):
    global CARDS
    card_to_id = {card.id: card for card in CARDS}
    ordered_cards = [card_to_id[id] for id in id_list if id in card_to_id]
    for card in CARDS:
        if card.id not in id_list:
            ordered_cards.append(card)
    CARDS = ordered_cards
@blueprint.route("/", methods=["GET"])
def get_all_cards():
    return render_template("htmx/cards/card_list.html", cards = CARDS)
@blueprint.route('/', methods=['POST'])
def create_card():
    title = request.form['title']
    content = request.form['content']
    newCard = Card(title, content)
    CARDS.insert(0, newCard)
    return render_template("htmx/cards/card_list.html",
                           cards=CARDS)

@blueprint.route("/<id>", methods=["DELETE"])
def delete_card(id):
    time.sleep(1) # just to show the spinner
    deleteCardById(id)
    return make_response("", 200)

@blueprint.route("/reorder", methods=["PATCH"])
def reorder_cards():
    ids = request.form.getlist("id")
    print(f"IDS {ids}")
    reorderCardsByIdList(ids)
    return render_template("htmx/cards/card_list.html",
                           cards=CARDS)