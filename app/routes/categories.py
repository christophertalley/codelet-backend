from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Set, Category

bp = Blueprint('categories', __name__, url_prefix='/categories')


# Error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.erreor)
    response.status_code = ex.status_code
    return response


# Return all categories
@bp.route('')
def categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])


# returns all sets in a category
@bp.route('/<int:category_id>/sets')
@cross_origin(headers=["Content-Type", "Authorization"])
def category_sets(category_id):
    category_info = Category.query.options(
        db.joinedload('sets')).get(category_id)
    return category_info.to_dict_sets(), 200


# Return single category by its id
@bp.route('/<int:category_id>')
@cross_origin(headers=["Content-Type", "Authorization"])
def category(category_id):  # returns cat info @category_id
    category = Category.query.get(category_id)
    return category.to_dict(), 200


# Create a new category
@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_category():
    data = request.json
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return category.to_dict(), 201
