from app.controllers.auth import validate_request

from flask import Blueprint, jsonify, request


read = Blueprint('read', __name__)


@read.route('/all', strict_slashes=False, methods=['POST'])
def read_all_bookmarks():
    """Fetches all the bookmarks for a given user"""
    response = dict()

    user = validate_request(request)

    if user is None:
        response['status'] = 'failure'
        response['message'] = 'Failed to validate request'
        response['code'] = 401
        return jsonify(response)

    try:
        bookmarks = []

        for bookmark in user.bookmarks:
            bookmark_data = {
                'name': bookmark.name,
                'url': bookmark.url,
                'tags': [tag.name for tag in bookmark.tags],
                'id': bookmark.id
            }
            bookmarks.append(bookmark_data)

        response['bookmarks'] = bookmarks
        response['status'] = 'success'
        response['message'] = 'Successfully retrieved all bookmarks'
        response['code'] = 200

    except Exception as e:
        response['status'] = 'failure'
        response['message'] = 'Failed to retrieve bookmarks'
        response['error'] = str(e)
        response['code'] = 400

    return jsonify(response)
