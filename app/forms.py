from app import db
from app.models import Creative, MediaType
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Optional


class ContactForm(FlaskForm):
	# TODO: max / min length
	# - also EmailField? or validators (on frontend too)
	email = StringField('email', validators=[ DataRequired() ])
	message = StringField('message', validators=[ DataRequired() ])

	submit_button = SubmitField('submit_button')



### ADMIN ###

class LoginForm(FlaskForm):
	_user = None
	email = StringField('email', validators=[ DataRequired() ])
	password = PasswordField('password', validators=[ DataRequired() ])

	def validate(self):
		self._user = Creative.query.filter_by(email=self.email.data).first()
		return super(LoginForm, self).validate()

	def validate_email(self, email):
		if self._user is None:
			raise ValidationError("Incorrect")

	def validate_password(self, password):
		if not self._user.check_password(password.data):
			raise ValidationError("Incorrect")

class CreateCreativeForm(FlaskForm):

	name = StringField('name', validators=[ DataRequired() ])
	about = StringField('about', validators=[ DataRequired() ])

	category = SelectField('category', coerce=int, validators=[ DataRequired() ])

	profile_image = FileField('profile_image')

	# TODO: make these have data=None if they're empty (len == 0)

	email = StringField('email', validators=[ DataRequired() ])
	password = PasswordField('password', validators=[ DataRequired() ])
	
	website = StringField('website', validators=[ Optional() ])

	instagram_url = StringField('instagram_url', validators=[ Optional() ])
	twitter_url = StringField('twitter_url', validators=[ Optional() ])
	facebook_url = StringField('facebook_url', validators=[ Optional() ])
	bandcamp_url = StringField('bandcamp_url', validators=[ Optional() ])
	reddit_url = StringField('reddit_url', validators=[ Optional() ])
	spotify_url = StringField('spotify_url', validators=[ Optional() ])
	apple_music_url = StringField('apple_music_url', validators=[ Optional() ])
	soundcloud_url = StringField('soundcloud_url', validators=[ Optional() ])

	submit_button = SubmitField('submit_button')


class CreateProjectForm(FlaskForm):

	name = StringField('name', validators=[ DataRequired() ])
	about = StringField('about', validators=[ DataRequired() ])

	profile_image = FileField('profile_image')



class CreateMediaForm(FlaskForm):

	caption = StringField('caption', validators=[ Optional() ])
	media_type = RadioField('media_type', coerce=int, validators=[ DataRequired() ])

	url = StringField('url', validators=[ Optional() ])
	media_image = FileField('media_image')

	def validate(self):
		self._media_type = MediaType(self.media_type.data)
		return super(CreateMediaForm, self).validate()

	def validate_media_type(self, email):
		if self._media_type is None:
			raise ValidationError("Invalid")

	def validate_url(self, url):
		if self._media_type != MediaType.image and len(url) == 0:
			raise ValidationError("Required")

	def validate_media_image(self, media_image):
		if self._media_type == MediaType.image and self.media_image.data is None:
			raise ValidationError("Required")