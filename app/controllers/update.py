from app import db
from app.models.bookmark import Bookmark, Tag
from app.controllers.auth import validate_request

from flask import Blueprint, jsonify, request

update = Blueprint('update', __name__)


@update.route('/update', strict_slashes=False, methods=['POST'])
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

            bookmark.tags = data['tags']

        db.session.commit()

        response['status'] = 'success'
        response['message'] = 'Updated existing bookmark'
        response['code'] = 201
    except Exception as e:
        response['message'] = 'An error has occurred'
        response['error'] = str(e)
        response['code'] = 400

    return jsonify(response)
