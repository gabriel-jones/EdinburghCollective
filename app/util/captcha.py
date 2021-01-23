import requests
from flask import current_app
from app.response import *


def validate_captcha(response_token, action_name):
	params = {
		"secret": current_app.config.get("CAPTCHA_SECRET"),
		"response": response_token
	}

	response = requests.post('https://www.google.com/recaptcha/api/siteverify', params=params)
	data = response.json()

	if 'success' not in data:
		raise APIException(APIException.unknown, 500)

	if not data['success'] or data['score'] < 0.5:
		raise APIException(APIException.invalidCaptcha, 400)