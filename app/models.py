from app import db, login
import enum
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


creative_media = db.Table('creative_media', 
	db.Column('creative_id', db.Integer, db.ForeignKey('creative.id')),
	db.Column('media_id', db.Integer, db.ForeignKey('media.id'))
)


class MediaType(enum.Enum):
	image = 0
	youtube = 1
	video_url = 2
	spotify = 3
	apple_music = 4

	@staticmethod
	def all():
		return [ MediaType.image, MediaType.youtube, MediaType.video_url, MediaType.spotify, MediaType.apple_music ] 


class Media(db.Model):
	__tablename__ = 'media'

	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, nullable=False, index=False, unique=False)
	type = db.Column(db.Enum(MediaType), nullable=False, index=False, unique=False)
	
	caption = db.Column(db.String, nullable=True, index=False, unique=False)
	url = db.Column(db.String, nullable=True, index=False, unique=False)
	
	creative = db.relationship('Creative', secondary=creative_media, back_populates='media', uselist=False)

	@property
	def media_url(self):
		if self.type == MediaType.image:
			return f'/static/img/uploads/{self.id}.jpg'
		return self.url

	@property
	def file_url(self):
		assert self.type == MediaType.image
		return 'app/' + self.media_url

	def __init__(self, type):
		self.created_at = datetime.datetime.utcnow()
		self.type = type

	def __repr__(self):
		return f'<Media #{self.id}>'


class Category(db.Model):
	__tablename__ = 'category'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, index=False, unique=False)

	creatives = db.relationship('Creative', back_populates='category')

	def __repr__(self):
		return f'<Category #{self.id}>'


@login.user_loader
def user_loader(id):
	return Creative.query.get(int(id))


class Creative(UserMixin, db.Model):
	__tablename__ = 'creative'

	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, nullable=False, index=False, unique=False)
	
	is_admin = db.Column(db.Boolean, server_default='false', nullable=False, index=False, unique=False)

	email = db.Column(db.String, nullable=False, index=False, unique=True)
	password = db.Column(db.String, nullable=False, index=False, unique=False)
	
	name = db.Column(db.String, nullable=False, index=False, unique=False)
	about = db.Column(db.String, nullable=True, index=False, unique=False)

	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	category = db.relationship('Category', foreign_keys=[category_id])

	profile_image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
	profile_image = db.relationship('Media', foreign_keys=[profile_image_id])

	website = db.Column(db.String, nullable=True, index=False, unique=False)
	
	instagram_url = db.Column(db.String, nullable=True, index=False, unique=False)
	twitter_url = db.Column(db.String, nullable=True, index=False, unique=False)
	facebook_url = db.Column(db.String, nullable=True, index=False, unique=False)
	bandcamp_url = db.Column(db.String, nullable=True, index=False, unique=False)
	reddit_url = db.Column(db.String, nullable=True, index=False, unique=False)
	spotify_url = db.Column(db.String, nullable=True, index=False, unique=False)
	apple_music_url = db.Column(db.String, nullable=True, index=False, unique=False)
	soundcloud_url = db.Column(db.String, nullable=True, index=False, unique=False)

	is_homepage = db.Column(db.Boolean, server_default='false', nullable=False, index=True, unique=False)

	projects = db.relationship('Project', back_populates='members')
	media = db.relationship('Media', secondary=creative_media, back_populates='creative')

	def __init__(self, name, category):
		self.created_at = datetime.datetime.utcnow()
		self.name = name
		self.category = category

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def __repr__(self):
		return f'<Creative #{self.id}>'


project_creatives = db.Table('project_creatives', 
	db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
	db.Column('creative_id', db.Integer, db.ForeignKey('creative.id'))
)

class Project(db.Model):
	__tablename__ = 'project'

	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, nullable=False, index=False, unique=False)

	created_by_id = db.Column(db.Integer, db.ForeignKey('creative.id'), nullable=False)
	created_by = db.relationship('Creative', foreign_keys=[created_by_id])

	profile_image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
	profile_image = db.relationship('Media', foreign_keys=[profile_image_id])

	name = db.Column(db.String, nullable=False, index=False, unique=False)
	about = db.Column(db.String, nullable=False, index=False, unique=False)
	
	members = db.relationship('Creative', secondary=project_creatives, back_populates='projects')

	def __init__(self, name, about):
		self.created_at = datetime.datetime.utcnow()
		self.name = name
		self.about = about

	def __repr__(self):
		return f'<Project #{self.id}>'


class Message(db.Model):
	__tablename__ = 'message'

	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, nullable=False, index=False, unique=False)

	email = db.Column(db.String, nullable=False, index=False, unique=False)
	message = db.Column(db.String, nullable=False, index=False, unique=False)
	
	def __init__(self, email, message):
		self.created_at = datetime.datetime.utcnow()
		self.email = email
		self.message = message

	def __repr__(self):
		return f'<Message #{self.id}>'