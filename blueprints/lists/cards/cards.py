from flask import Blueprint, render_template, make_response, request, url_for, abort
from domain.Card import Card
from domain.CardList import CardList
import time

cards_blueprint = Blueprint("cards",
                      __name__,
                      template_folder="../templates/htmx/cards/",
                      url_prefix="/cards")

@cards_blueprint.route("/", methods=["GET"])
def get_cards():
    return "THAT IS lists/cards"