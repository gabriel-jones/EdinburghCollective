from app import db
from app.models import *
from app.forms import *
from flask import Blueprint, abort, render_template, request, redirect, url_for, send_from_directory
from flask_login import current_user, login_required, login_user


blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=["GET"])
def home():
	projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
	creatives = Creative.query.filter_by(is_homepage=True).limit(3).all()

	return render_template('home.html.j2', 
		home_creatives=creatives,
		projects=projects
	)


@blueprint.route("/creatives", methods=["GET"])
@blueprint.route("/creatives/<string:category_name>", methods=["GET"])
def creatives(category_name=None):
	category = None

	creatives = Creative.query
	if category_name != None:
		category = Category.query.filter_by(name=category_name).first()
		if category is None:
			abort(404)
		creatives = creatives.filter_by(category_id=category.id)
	
	creatives = creatives.all()

	categories = Category.query.all()

	return render_template('creatives.html.j2', 
		creatives=creatives,
		categories=categories,
		active_category=category
	)


@blueprint.route("/creatives/<int:creative_id>", methods=["GET"])
def view_creative(creative_id):
	creative = Creative.query.get(creative_id)
	if creative is None:
		abort(404)

	return render_template('view_creative.html.j2', 
		creative=creative
	)


@blueprint.route("/projects", methods=["GET"])
def projects():
	projects = Project.query.all()

	return render_template('projects.html.j2', 
		projects=projects
	)


@blueprint.route("/projects/<int:project_id>", methods=["GET"])
def view_project(project_id):
	project = Project.query.get(project_id)
	if project is None:
		abort(404)

	return render_template('view_project.html.j2', 
		project=project
	)


@blueprint.route("/contact", methods=["GET", "POST"])
def contact():
	form = ContactForm()
	did_submit = False

	if form.validate_on_submit():
		did_submit = True
		# TODO: captcha, email to nat+fraz?
		msg = Message(form.email.data, form.message.data)
		db.session.add(msg)
		db.session.commit()

	return render_template('contact.html.j2', 
		form=form,
		did_submit=did_submit
	)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.admin'))

	form = LoginForm()

	if form.validate_on_submit():
		login_user(form._user)
		return redirect(url_for('main.admin'))

	return render_template('login.html.j2',
		form=form
	)


### ADMIN ###

@blueprint.route("/admin", methods=["GET"])
def admin():
	return render_template('admin/index.html.j2')


@blueprint.route("/admin/project", methods=["GET", "POST"])
@login_required
def create_project():
	form = CreateProjectForm()

	if form.validate_on_submit():
		project = Project(form.name.data, form.about.data)
		project.created_by = current_user
		db.session.add(project)
		db.session.flush()

		current_user.projects.append(project)
		db.session.commit()

		return redirect('main.view_project', project_id=project.id)

	return render_template('admin/create_project.html.j2',
		form=form
	)


@blueprint.route("/admin/media", methods=["GET", "POST"])
@login_required
def create_media():
	form = CreateMediaForm()
	form.media_type.choices = [ (x.value, x.name) for x in MediaType.all() ]

	if form.validate_on_submit():
		media = Media(MediaType.image)
		db.session.add(media)
		db.session.flush()

		# TODO: image stuff

		current_user.media.append(media)
		db.session.commit()

		return redirect('main.view_creative', creative_id=current_user.id)

	return render_template('admin/create_media.html.j2',
		form=form
	)


@blueprint.route("/admin/creative", methods=["GET", "POST"])
@login_required
def create_creative():
	if not current_user.is_admin:
		abort(401)

	form = CreateCreativeForm()
	form.category.choices = [ (category.id, category.name) for category in Category.query.all() ]

	if form.validate_on_submit():
		category = Category.query.get(form.category.data)
		if category is None:
			abort(400)

		creative = Creative(form.name.data, category)
		creative.about = form.about.data

		print(form.profile_image.data)
		print(form.profile_image.raw_data)
		for file in form.profile_image.raw_data:
			media = Media(MediaType.image)
			db.session.add(media)
			db.session.flush()

			creative.profile_image = media

			file.save(media.file_url)
		
		creative.email = form.email.data
		creative.set_password(form.password.data)
		creative.website = form.website.data
		creative.instagram_url = form.instagram_url.data
		creative.twitter_url = form.twitter_url.data
		creative.facebook_url = form.facebook_url.data
		creative.bandcamp_url = form.bandcamp_url.data
		creative.reddit_url = form.reddit_url.data
		creative.spotify_url = form.spotify_url.data
		creative.apple_music_url = form.apple_music_url.data
		creative.soundcloud_url = form.soundcloud_url.data
		
		db.session.add(creative)
		db.session.commit()

		return redirect(url_for('main.view_creative', creative_id=creative.id))

	return render_template('admin/create_creative.html.j2',
		form=form
	)