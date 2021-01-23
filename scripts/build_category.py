import os
import json
import string
from app import db
from app.models import Category
from flask_script import Command


class BuildCategoryCommand(Command):
	def run(self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'category.json')
		with open(path) as file:
			categories = json.load(file)
			for category_json in categories:
				existing = Category.query.get(category_json['id'])
				if existing is not None:
					existing.name = category_json['name']
				else:
					category = Category(
						id=category_json['id'],
						name=category_json['name']
					)
					db.session.add(category)
			db.session.commit()
			print('[*] Categoroes rebuilt')