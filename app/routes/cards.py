from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Card, Set
import requests
import json

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


# update a card
@bp.route('/<int:card_id>', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def update_card(card_id):
    token = request.headers.get('Authorization')
    req = requests.get('https://codelet-app.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    userId = User.query.filter_by(email=userInfo['email']).first().id

    card = Card.query.get(card_id)
    parentSet = Set.query.get(card.set_id)
    creator_id = parentSet.user_id
    if userId == creator_id:
        data = request.json
        if data.get('definition'):
            card.definition = data['definition']
        if data.get('term'):
            card.term = data['term']

        db.session.commit()
        return card.to_dict(), 201


# Delete a card
@bp.route('/<int:card_id>', methods=['DELETE'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_card(card_id):
    # data = request.json

    # gets decodes userinfo out of token using auth0 api
    token = request.headers.get('Authorization')
    req = requests.get('https://codelet-app.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    userId = User.query.filter_by(email=userInfo['email']).first().id

    card = Card.query.get(card_id)
    parentSet = Set.query.get(card.set_id)
    creator_id = parentSet.user_id
    if userId == creator_id:
        db.session.delete(card)
        db.session.commit()
        return 'Deleted', 204
    else:
        return 'Authorization denied', 401
