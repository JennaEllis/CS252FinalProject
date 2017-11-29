from app import db
from app.models.bookmark import Bookmark, Tag
from app.controllers.auth import validate_request

from flask import Blueprint, jsonify, request

update = Blueprint('update', __name__)


@update.route('/', strict_slashes=False, methods=['POST'])
def update_bookmark():
    """Update bookmark for the given user"""
    response = dict()
    response['status'] = 'failure'

    user = validate_request(request)

    if user is None:
        response['message'] = 'Failed to validate request'
        response['code'] = 401
        return jsonify(response)

    data = request.get_json()
    print(str(data))

    try:
        bookmark_id = data['id']
        bookmark = Bookmark.query.filter_by(id=bookmark_id).first()

        if bookmark is None or bookmark not in user.bookmarks:
            response['status'] = 'failure'
            response['message'] = 'Could not update bookmark'
            response['code'] = 401
            return jsonify(response)

        if data['name'] is not None:
            bookmark.name = data['name']

        if data['url'] is not None:
            bookmark.url = data['url']

        if data['tags'] is not None:
            if len(data['tags']) > 10:
                response['status'] = 'failure'
                response['message'] = 'Invalid number of tags'
                response['code'] = 400
                return jsonify(response)

            tags = data['tags']
            tags[:] = [x for x in tags if x != '$_$_$']

            for tag in tags:
                tag_search = Tag.query.filter_by(name=tag.lower()).first()

                if tag_search is not None:
                    continue

                new_tag = Tag(name=tag.lower())

                db.session.add(new_tag)
                db.session.commit()

            valid_tags = [Tag.query.filter_by(name=tag).one() for tag in tags]

            bookmark.tags = valid_tags

        db.session.commit()

        response['status'] = 'success'
        response['message'] = 'Updated existing bookmark'
        response['code'] = 201
    except Exception as e:
        response['message'] = 'An error has occurred'
        response['error'] = str(e)
        response['code'] = 400

    print(response)
    return jsonify(response)
