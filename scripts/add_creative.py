import os
import json
import string
from app import db
from app.models import Creative, Category
from flask_script import Command, Option


class AddCreativeCommand(Command):

	option_list = (
		Option('--name', '-n', dest='_name'),
		Option('--category_id', '-c', dest='_category_id'),
		Option('--email', '-e', dest='_email'),
		Option('--password', '-p', dest='_password'),
	)
	def run(self, _name, _category_id, _email, _password):
		category = Category.query.get(_category_id)
		if category is None:
			print('[!] Category id not found')
			return
		creative = Creative(_name, category)
		creative.email = _email
		creative.set_password(_password)
		db.session.add(creative)
		db.session.commit()
