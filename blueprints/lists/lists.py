from flask import Blueprint, render_template, make_response, request, url_for, abort
import blueprints.lists.cards.cards as cards
from domain.Card import Card
from domain.CardList import CardList
import time

lists_blueprint = Blueprint("lists",
                            __name__,
                            template_folder="../templates/htmx/cards/",
                            url_prefix="/lists")
lists_blueprint.register_blueprint(cards.cards_blueprint)

LISTS = {}

@lists_blueprint.route("/", methods=["GET"])
def test_get():
    return f"HI, THIS IS lists/ url for {url_for('lists.cards.get_cards')}"
@lists_blueprint.route("/list-creation-form", methods=["GET"])
def get_list_creation_form():
    if "HX-Request" not in request.headers:
        abort(403)
    return render_template("list_creation_form.html")

@lists_blueprint.route("/", methods=["POST"])
def create_card_list():
    print(f"CREATE LIST POST {request.form.items()}")
    list_name = request.form.get("list-name")
    new_list = CardList(list_name)
    list_id = new_list.get_id()
    LISTS[list_id] = new_list
    return render_template("new_card_list.html",
                           card_list = LISTS[list_id],
                           title=request.form.get("list-name"),
                           hx_put_url=url_for("lists.reorder_cards", list_id=list_id))

@lists_blueprint.route("/<string:list_id>", methods=["GET"])
def get_card_list(list_id):
    if list_id not in LISTS.keys():
        abort(404)
    return render_template("new_card_list.html",
                           card_list=LISTS[list_id],
                           title=request.form.get("list"),
                           hx_put_url=url_for("lists.reorder_cards", list_id=list_id))
@lists_blueprint.route("/reorder/<string:list_id>", methods=["PUT"])
def reorder_cards(list_id):
    if list_id not in LISTS.keys():
        abort(404)
    ordered_ids = request.form.getlist("id")
    print(f"IDS {ordered_ids}")
    card_list = LISTS[list_id]
    card_list.reorderCardsByIdList(ordered_ids)
    return render_template("card_list.html",
                           card_list=card_list,
                           hx_put_url=url_for("lists.reorder_cards", list_id=list_id))

