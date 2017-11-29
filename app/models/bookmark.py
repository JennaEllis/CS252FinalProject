from app import db


tags_bookmarks = db.Table(
    'tags_bookmarks',
    db.Column('bookmark_id', db.Integer(), db.ForeignKey('bookmarks.id'), primary_key=True),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id'), primary_key=True)
)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(80))


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    url = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    tags = db.relationship(
        'Tag', secondary=tags_bookmarks,
        backref=db.backref('bookmarks', lazy=True)
    )
