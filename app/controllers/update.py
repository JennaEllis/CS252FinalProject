from app import db
from app.models.bookmark import Bookmark, Tag
from app.controllers.auth import validate_request

from flask import Blueprint, jsonify, request

update = Blueprint('update', __name__)

@update.route('/update', methods=['POST'])
def update_bookmark():
	"""Update bookmark for the given user"""
	response = dict()
	response['status'] = 'failure'

	user = validate_request(request)

	if use is None:
		response['message'] = 'Failed to validate request'
		response['code'] = 401
		return jsonify(response)

	data = request.get_json()

	try:
		# doing some dank bookmark updating here 




		response['status'] = 'success'
		response['message'] = 'Updated existing bookmark'
		response['code'] 201
	except Exception as e:
		response['message'] = 'An error has occurred'
		response['error'] = str(e)
		response['code'] = 400

	return jsonify(response)
