from app import db

from flask_security import RoleMixin, UserMixin


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'), primary_key=True)
)


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime)

    active = db.Column(db.Boolean(), default=False)
    authenticated = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy=True)
    )

    def is_authenticated(self):
        """Determines if the user is authenticated"""
        return self['authenticated']

    def is_active(self):
        """Determines if the user is currently active"""
        return self['Active']

    def is_anonymous(self):
        """Determines if the user is anonymous"""
        return False

    def get_id(self):
        """Returns the id for the user"""
        return self.id
