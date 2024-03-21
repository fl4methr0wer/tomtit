from flask import Blueprint, render_template, make_response, request, url_for, abort
from domain.Card import Card
import time

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

blueprint = Blueprint("cards", __name__,
                      url_prefix="/cards",
                      template_folder="../templates/htmx/cards/")

@blueprint.route("/list-creation-form", methods=["GET"])
def get_list_creation_form():
    if "HX-Request" not in request.headers:
        abort(403)
    return render_template("list_creation_form.html")
@blueprint.route("/list", methods=["POST"])
def create_card_list():
    print(f"CREATE LIST POST {request.form}")
    local_cards = [Card("local card1", ""),
                   Card("local card2", "content2")]
    print(f"CREATE LIST POST {request.form.items()}")
    return render_template("new_card_list.html",
                           cards=local_cards,
                           title=request.form.get("list-name"),
                           hx_put_url=url_for("cards.reorder_cards"))

@blueprint.route("/card-creation-form", methods=["GET"])
def get_card_creation_form():
    if "HX-Request" not in request.headers:
        abort(304)
    return render_template("card_creation_form.html")

@blueprint.route("/", methods=["GET"])
def get_all_cards():
    return render_template("card_list.html",
                           hx_put_url=url_for("cards.reorder_cards"),
                           cards=CARDS)
@blueprint.route('/', methods=['POST'])
def create_card():
    print(f"URL FOR HX-PUT : {url_for('cards.reorder_cards')}")
    title = request.form['title']
    content = request.form['content']
    newCard = Card(title, content)
    CARDS.insert(0, newCard)
    return render_template("card_list.html",
                           hx_put_url=url_for('cards.reorder_cards'),
                           cards=CARDS)

@blueprint.route("/<string:id>", methods=["DELETE"])
def delete_card(id):
    time.sleep(1) # just to show the spinner
    deleteCardById(id)
    return make_response("", 200)

@blueprint.route("/reorder", methods=["PUT"])
def reorder_cards():
    ordered_ids = request.form.getlist("id")
    print(f"IDS {ordered_ids}")
    reorderCardsByIdList(ordered_ids)
    return render_template("card_list.html",
                           hx_put_url=url_for('cards.reorder_cards'),
                           cards=CARDS)