from flask import Blueprint, render_template, make_response, request, url_for, abort
from domain.Card import Card
from domain.CardList import CardList
import time

# LISTS = {
#     "test" : CardList("testCardList", [Card("testcard1", "testContent1"), Card("testcard2", "testcontent2")])
# }
LISTS = {}

blueprint = Blueprint("lists", __name__,
                      url_prefix="/lists",
                      template_folder="../templates/htmx/cards/")

@blueprint.route("/board", methods=["GET"])
def get_board():
    lists = [list for id, list in LISTS.items()]
    print("GET /board")
    print(f"LISTS VALUES:{[str(list) for list in lists] }")
    return render_template("board.html", card_lists=lists)
@blueprint.route("/list-creation-form", methods=["GET"])
def get_list_creation_form():
    if "HX-Request" not in request.headers:
        abort(403)
    return render_template("list_creation_form.html",
                           hx_post_url=url_for("lists.create_card_list"))
@blueprint.route("/", methods=["POST"])
def create_card_list():
    print(f"CREATE LIST POST REQUEST {request.form.get('list-name')}")
    list_name = request.form.get("list-name")
    new_list = CardList(list_name)
    list_id = new_list.get_id()
    LISTS[list_id] = new_list
    print(f"CREATED LISTS: {[str(list) for list in LISTS.values()]}")
    print(f"SENDING LIST: {LISTS[list_id]}")
    return render_template("new_card_list.html",
                           card_list = new_list,
                           hx_put_url=url_for("lists.reorder_card_list"))

@blueprint.route("/", methods=["PUT"])
@blueprint.route("/<string:list_id>", methods=["PUT"])
def reorder_card_list(list_id: str):
    list = LISTS[list_id]
    if None == list:
        abort(404)
    list.reorder_cards_by_id_list(request.form.getlist("id"))
    return render_template("new_card_list.html",
                           card_list = list,
                           hx_put_url=url_for("lists.reorder_card_list"))

@blueprint.route("/<string:list_id>/cards/", methods=["POST"])
def create_card_in_list(list_id):
    title = request.form["title"]
    if title == "":
        abort(403)
    content = request.form["content"]
    new_card = Card(title, content)
    card_list = LISTS[list_id]
    card_list.add_card(new_card)
    return render_template("new_card_list.html",
                           card_list = card_list,
                           hx_put_url=url_for("lists.reorder_card_list"))

@blueprint.route("/<string:list_id>/cards/<string:card_id>", methods=["DELETE"])
def delete_card(list_id, card_id):
    print(f"DELETE lists/<list_id>/cards/<card_id>")
    time.sleep(0.1) # just to show the spinner
    list = LISTS[list_id]
    list.delete_card_by_id(card_id)
    return make_response("", 200)

#=====================#
# @blueprint.route("/card-creation-form", methods=["GET"])
# def get_card_creation_form():
#     if "HX-Request" not in request.headers:
#         abort(304)
#     return render_template("card_creation_form.html")
#
# @blueprint.route("/", methods=["GET"])
# def get_all_cards():
#     return render_template("card_list.html",
#                            hx_put_url=url_for("reorder_cards"),
#                            cards=CARDS)
# @blueprint.route('/', methods=['POST'])
# def create_card():
#     print(f"URL FOR HX-PUT : {url_for('cards.reorder_cards')}")
#     title = request.form['title']
#     content = request.form['content']
#     newCard = Card(title, content)
#     CARDS.insert(0, newCard)
#     return render_template("card_list.html",
#                            hx_put_url=url_for('reorder_cards'),
#                            cards=CARDS)
#
# @blueprint.route("/<string:id>", methods=["DELETE"])
# def delete_card(id):
#     time.sleep(1) # just to show the spinner
#     #deleteCardById(id)
#     return make_response("", 200)

# @blueprint.route("/reorder", methods=["PUT"])
# def reorder_cards():
#     ordered_ids = request.form.getlist("id")
#     card_list = LISTS[]
#     print(f"IDS {ordered_ids}")
#     reorderCardsByIdList(ordered_ids)
#     return render_template("card_list.html",
#                            hx_put_url=url_for('reorder_cards'),
#                            cards=CARDS)