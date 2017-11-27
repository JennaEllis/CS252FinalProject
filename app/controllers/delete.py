from app import db
from app.models.bookmark import Bookmark, Tag
from app.controllers.auth import validate_request

from flask import Blueprint, jsonify, request

delete = Blueprint('delete', __name__)


@delete.route('/', strict_slashes=False, methods=['POST'])
def delete_bookmark():
    """Deletes a bookmark for the given user"""
    response = dict()
    response['status'] = 'failure'

    user = validate_request(request)

    if user is None:
        response['messsage'] = 'Failed to validate request'
        response['code'] = 401
        return jsonify(response)

    data = request.get_json()

    try:
        bookmark_id = data['id']

        bookmark = Bookmark.query.filter_by(id=bookmark_id).first()

        if bookmark not in user.bookmarks:
            response['status'] = 'failure'
            response['message'] = 'Cannot delete that bookmark'
            response['code'] = 401
            return jsonify(response)

        user.bookmarks.remove(bookmark)
        db.session.commit()

        response['status'] = 'success'
        response['message'] = 'Deleted a bookmark'
        response['code'] = 200

    except Exception as e:
        response['message'] = 'An error has occurred'
        response['error'] = str(e)
        response['code'] = 400

    return jsonify(response)
