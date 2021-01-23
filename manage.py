import os
import config
from app import create_app

application = create_app(config.Config)

from flask_script import Manager
manager = Manager(application)

from flask_migrate import MigrateCommand
manager.add_command('db', MigrateCommand)

from scripts.build_category import BuildCategoryCommand
manager.add_command('build_category', BuildCategoryCommand)

from scripts.add_creative import AddCreativeCommand
manager.add_command('add_creative', AddCreativeCommand)

if __name__ == '__main__':
	manager.run()