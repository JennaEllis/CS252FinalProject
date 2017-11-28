from app import db
from app.models.bookmark import Bookmark, Tag
from app.controllers.auth import validate_request

from flask import Blueprint, jsonify, request


create = Blueprint('create', __name__)


@create.route('/', strict_slashes=False, methods=['POST'])
def create_bookmark():
    """Creates a new bookmark for the given user"""
    response = dict()
    response['status'] = 'failure'

    user = validate_request(request)

    if user is None:
        response['message'] = 'Failed to validate request'
        response['code'] = 401
        return jsonify(response)

    data = request.get_json()

    try:
        url = data['url']
        name = data['name']
        tags = data['tags']
        tags[:] = [x for x in tags if x != '$_$_$']

        # create the new tags
        for tag in tags:
            tag_search = Tag.query.filter_by(name=tag.lower()).first()

            if tag_search is not None:
                continue

            new_tag = Tag(name=tag.lower())

            db.session.add(new_tag)
            db.session.commit()

        valid_tags = [Tag.query.filter_by(name=tag).one() for tag in tags]

        bookmark = Bookmark(url=url, name=name, tags=valid_tags)
        db.session.add(bookmark)

        user.bookmarks.append(bookmark)

        db.session.commit()

        response['status'] = 'success'
        response['message'] = 'Added a new bookmark'
        response['code'] = 201
    except Exception as e:
        response['message'] = 'An error has occurred'
        response['error'] = str(e)
        response['code'] = 400

    return jsonify(response)
