from flask import Flask, render_template, url_for, request
from util import json_response

import data_handler, persistence

app = Flask(__name__)


@app.route("/")
def index():
    """
    This is a one-pager which shows all the boards and cards
    """
    return render_template('index.html')


@app.route("/get-boards", methods=["GET", "POST"])
@json_response
def get_boards():
    """
    All the boards
    """
    if request.method == "POST":
        data = request.get_json()
        data_dict = dict(data.items())
        persistence.save_new_board_data(data_dict)
        return data_dict
    else:
        list_of_boards = data_handler.get_boards()
        for board in list_of_boards:
            board['statuses'] = board['statuses'].split(",")
        return list_of_boards


@app.route("/get-statuses", methods=['GET', 'POST'])
@json_response
def get_statuses():
    """
    All the boards
    """
    if request.method == 'GET':
        return data_handler.get_statuses()
    elif request.method == 'POST':
        data = request.get_json()
        data_dict = dict(data.items())
        persistence.save_new_status(data_dict)
        return data_dict
    else:
        render_template('index.html')


@app.route("/get-cards/<int:board_id>", methods=["GET", "POST"])
@json_response
def get_cards_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    cards = persistence.get_cards()
    last_card_id = len(cards)

    if request.method == "POST":
        data = request.get_json()
        data_dict = dict(data.items())
        data_dict['id'] = last_card_id + 1
        persistence.save_new_card_data(data_dict)
        return data_dict
    else:
        return data_handler.get_cards_for_board(board_id)


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
