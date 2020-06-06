from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User

bp = Blueprint("users", __name__, url_prefix='/users')


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.route('')
def user():
    return "get user"


@bp.route('/private')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def privateUser():
    return "private user endpoint"


@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def updateUser():
    if request.method == 'POST':
        body = request.json
        # return body['email']
        # checks if there there is user in db
        db_user = User.query.filter_by(email=body['email']).first()
        if db_user:
            db_user.nickname = body['nickname']
            return jsonify({'userId': db_user.id}), 201
        else:  # no user exists so we create a new user
            new_user = User(email=body['email'],
                            nickname=body['nickname']
                            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user), 201
