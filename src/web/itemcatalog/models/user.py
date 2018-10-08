from . import db
from itemcatalog import login_manager
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id user to retrieve

    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def __repr__(self):
        return '<User {}>'.format(self.name)


class UserAuth(db.Model, OAuthConsumerMixin):

    __tablename__ = 'userauth'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)