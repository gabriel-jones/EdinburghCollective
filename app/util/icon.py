import os
from config import Config
import re


def load_icons():
	ICONS = {}
	url = os.path.join(Config.APP_ROOT, 'static', 'icons')
	for item in os.listdir(url):
		if item.endswith('svg'):
			with open(os.path.join(url, item), 'r') as f:
				contents = f.read()
				contents = re.search(r'(?=<path)(.*?)(?=\/|fill)', contents)
				name = item.split('.')[0]
				ICONS[name] = contents.group() + '/>'
	return ICONS