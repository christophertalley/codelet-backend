from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Card

bp = Blueprint("cards", __name__, url_prefix='/cards')


# Error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Return a single card by its id
@bp.route('/<int:card_id>')
@cross_origin(headers=["Content-Type", "Authorization"])
def card(card_id):  # returns card info @card_id
    card = Card.query.get(card_id)
    print(card)
    return card.to_dict(), 200


# Create a new card
@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_card():
    data = request.json
    card = Card(term=data['term'],
                definition=data['definition'],
                set_id=data['set_id']
                )
    db.session.add(card)
    db.session.commit()
    return card.to_dict(), 201
