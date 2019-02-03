from datetime import datetime
from flask import render_template, session, redirect, url_for,flash
from flask_login import login_required

from . import main
from .forms import NameForm, EditProfileForm
from .. import db
from ..models import User
from flask import abort


@main.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())


@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/user/<username>/edit', methods=['GET', 'POST'])
def edit(username):
    form = EditProfileForm()
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Succeed.')
        return render_template('index.html', user=user,current_time=datetime.utcnow())

    return render_template('edit.html', form=form,user=user)
