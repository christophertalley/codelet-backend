from app.search import add_to_index, remove_from_index, query_index
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

favorites_table = db.Table('favorites', db.Model.metadata,
    db.Column("set_id", db.Integer, db.ForeignKey('sets.id'), nullable=False),  # noqa
    db.Column("user_id", db.Integer, db.ForeignKey('users.id'), nullable=False))  # noqa


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False)

    sets = db.relationship('Set', back_populates='user')
    favorites = db.relationship(
        'Set', secondary=favorites_table)
    votes = db.relationship('Vote', back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'userSets': [set.to_dict() for set in self.sets],
            'favoriteSets': [favorite.to_dict() for favorite in self.favorites]
        }

    def to_dict_favorites(self):
        return {
            'id': self.id
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

    def to_dict_sets(self):
        return {
            'id': self.id,
            'name': self.name,
            'sets': [set.to_dict() for set in self.sets]
        }


class Set(SearchableMixin, db.Model):
    __tablename__ = 'sets'
    __searchable__ = ['title', 'description']

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
    votes = db.relationship('Vote', back_populates='set')
    favorites = db.relationship('User', secondary=favorites_table)

    def to_dict(self):
        num_upvotes = 0
        for vote in self.votes:
            if vote.is_upvote is True:
                num_upvotes += 1
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
            'favorites': [favorite.to_dict_favorites() for favorite in self.favorites],
            'num_upvotes': num_upvotes
        }


class Card(SearchableMixin, db.Model):
    __tablename__ = 'cards'
    __searchable__ = ['term', 'definition']

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
