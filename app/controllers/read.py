from app.controllers.auth import validate_request
from app.models.bookmark import Tag

from flask import Blueprint, jsonify, request


read = Blueprint('read', __name__)


@read.route('/tag=<tag>', methods=['POST'])
def filter_by_tag(tag):
    """Fetches all bookmarks with the matching tag"""
    response = dict()

    user = validate_request(request)

    if user is None:
        response['status'] = 'failure'
        response['message'] = 'Failed to validate request'
        response['code'] = 401
        return jsonify(response)

    try:
        tag = Tag.query.filter_by(name=tag).first()

        if tag is None:
            response['status'] = 'failure'
            response['message'] = 'No matching bookmarks'
            response['code'] = 200
            return jsonify(response)

        bookmarks = []

        for bookmark in user.bookmarks:
            if tag not in bookmark.tags:
                continue

            bookmark_data = {
                'name': bookmark.name,
                'url': bookmark.url,
                'tags': [tag.name for tag in bookmark.tags],
                'id': bookmark.id
            }
            bookmarks.append(bookmark_data)

        response['bookmarks'] = bookmarks
        response['status'] = 'success'
        response['message'] = 'Successfully retrieved matching bookmarks'
        response['code'] = 200

    except Exception as e:
        response['status'] = 'failure'
        response['message'] = 'Failed to retrieve bookmarks'
        response['error'] = str(e)
        response['code'] = 400

    return jsonify(response)


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
