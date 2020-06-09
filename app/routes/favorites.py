from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Set, Card, Vote
import requests
import json

bp = Blueprint('favorites', __name__, url_prefix='/sets')


# Error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.erreor)
    response.status_code = ex.status_code
    return response


# @bp.route('/<int:set_id>/favorites', methods=['PATCH'])
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
# def create_favorite(set_id):
#     # gets decodes userinfo out of token using auth0 api
#     token = request.headers.get('Authorization')
#     req = requests.get('https://codelet-app.auth0.com/userinfo',
#                        headers={'Authorization': token}).content
#     userInfo = json.loads(req)
#     userId = User.query.filter_by(email=userInfo['email']).first().id
#     dbFavorite = Favorite.query.filter_by(
#         user_id=userId, set_id=set_id).first()

#     if dbFavorite:
#         db.session.delete(dbFavorite)
#         db.session.commit()
#         return "Deleted", 204
#     else:
#         new_favorite = Favorite(user_id=userId, set_id=set_id)
#         db.session.add(new_favorite)
#         db.session.commit()
#         return "Created favorite", 201
