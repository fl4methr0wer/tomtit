from flask import Flask, render_template
from blueprints import cards
from blueprints.lists import lists
from blueprints.lists.cards import cards
import os

app = Flask(__name__)

#app.register_blueprint(cards.blueprint)
app.register_blueprint(lists.lists_blueprint)
app.register_blueprint(cards.cards_blueprint)

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
