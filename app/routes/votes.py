from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Set, Card, Vote
import requests
import json

bp = Blueprint('votes', __name__, url_prefix='/sets')


# Error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.erreor)
    response.status_code = ex.status_code
    return response


# Updates votes
@bp.route('/<int:set_id>/votes', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_vote(set_id):
    # upvote from body
    isUpvote = request.json['isUpvote']

    # gets decodes userinfo out of token using auth0 api
    token = request.headers.get('Authorization')
    req = requests.get('https://codelet-app.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    userId = User.query.filter_by(email=userInfo['email']).first().id
    dbVote = Vote.query.filter_by(user_id=userId, set_id=set_id).first()
    if dbVote:
        if isUpvote == dbVote.is_upvote:
            db.session.delete(dbVote)
            db.session.commit()
            return "Deleted", 204
        else:
            dbVote.is_upvote = not dbVote.is_upvote
            db.session.commit()
            return "Switched Vote", 206
    else:
        new_vote = Vote(user_id=userId, set_id=set_id, is_upvote=isUpvote)
        db.session.add(new_vote)
        db.session.commit()
        return "Created vote", 201
