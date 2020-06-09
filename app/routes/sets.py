from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Set, Card
import requests
import json

bp = Blueprint('sets', __name__, url_prefix='/sets')


# Error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Return all sets
@bp.route('')
def sets():
    sets = Set.query.all()
    return jsonify([set.to_dict() for set in sets])

# Return a single set by its id


@bp.route('/<int:set_id>')
@cross_origin(headers=["Content-Type", "Authorization"])
def set(set_id):  # returns set info @set_id
    set = Set.query.get(set_id)
    return set.to_dict(), 200


# Route to return all cards in a set
@bp.route('/<int:set_id>/cards')
@cross_origin(headers=["Content-Type", "Authorization"])
def set_cards(set_id):  # returns set info @set_id
    cards = Card.query.filter_by(set_id=set_id).all()
    return jsonify([card.to_dict() for card in cards])


# Create new set
@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_set():
    data = request.json

    # gets decodes userinfo out of token using auth0 api
    token = request.headers.get('Authorization')
    req = requests.get('https://codelet-app.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    userId = User.query.filter_by(email=userInfo['email']).first().id
    set = Set(title=data['title'],
              description=data['description'],
              category_id=data['category_id'],
              user_id=userId,
              created_at=data['created_at'],
              )
    db.session.add(set)
    db.session.commit()
    return set.to_dict(), 201
