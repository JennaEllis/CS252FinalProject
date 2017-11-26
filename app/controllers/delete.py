from app import db
from app.models.bookmark import Bookmark, Tag
from app.controllers.auth import validate_request

from flask import BluePrint, jsonify, request

create = Blueprint('delete', __name__)

@create.route('/remove', methods=['POST'])
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
		# trying to delete the bookmark here
		
		response['status'] = 'success'
		response['message'] = 'Deleted a bookmark'
		response['code'] = 201

	except Exception as e:
		response['message'] = 'An error has occurred'
		response['error'] = str(e)
		response['code'] = 400

	return jsonify(response)
