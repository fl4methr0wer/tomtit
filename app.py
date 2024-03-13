from flask import Flask, render_template
from blueprints import card

app = Flask(__name__)

app.register_blueprint(card.blueprint)

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
