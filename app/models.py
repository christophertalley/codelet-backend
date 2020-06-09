from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False)

    sets = db.relationship('Set', back_populates='user')
    favorites = db.relationship('Favorite', back_populates='user')
    votes = db.relationship('Vote', back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'userSets': [set.to_dict() for set in self.sets],
            'favoriteSets': [favorite.set_id for favorite in self.favorites]
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    sets = db.relationship('Set', back_populates='category')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Set(db.Model):
    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(51), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='sets')
    category = db.relationship('Category', back_populates='sets')
    cards = db.relationship('Card', back_populates='set')
    favorites = db.relationship('Favorite', back_populates='set')
    votes = db.relationship('Vote', back_populates='set')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'author': self.user.nickname,  # returns nickname from user model
            # returns number of cards in set from relationship
            'card_count': len(self.cards),
            # returns votes info list from votes relationship
            'votes': [vote.to_dict() for vote in self.votes],
            # returns favorites info list
            'favorites': [favorite.to_dict() for favorite in self.favorites]

        }


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'), nullable=False)

    set = db.relationship('Set', back_populates='cards')

    def to_dict(self):
        return {
            'id': self.id,
            'term': self.term,
            'definition': self.definition,
            'set_id': self.set_id,
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='favorites')
    set = db.relationship('Set', back_populates='favorites')

    def to_dict(self):
        return {
            'id': self.id,
            'set_id': self.set_id,
            'user_id': self.user_id,
            # 'sets': self.set.to_dict_favorites()
        }

    def relations_to_dict(self):
        return {
            'sets': self.set.to_dict()
        }


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_upvote = db.Column(db.Boolean)

    user = db.relationship('User', back_populates='votes')
    set = db.relationship('Set', back_populates='votes')

    def to_dict(self):
        return {
            'id': self.id,
            'set_id': self.set_id,
            'user_id': self.user_id,
            'is_upvote': self.is_upvote
        }
