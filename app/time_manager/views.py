from . import time_manager
from flask_login import login_required, current_user
from .forms import AffairRegistrationForm
from ..models import Affair, Post, User
from .. import db
from flask import flash, redirect, url_for, render_template, request, current_app


@time_manager.route('/user/register-affair', methods=['GET', 'POST'])
@login_required
def register_affair():
    form = AffairRegistrationForm()
    if form.validate_on_submit():
        start_from = form.start_from.data or 0
        process_status = form.start_from.data or 0
        affair = Affair(name=form.name.data,
                        workload=int(form.workload.data),
                        start_from=int(start_from),
                        process_status=int(process_status),
                        description=form.description.data,
                        user=current_user._get_current_object()
                        )
        post = Post(body="Start affair [{}].".format(form.name.data), author=current_user._get_current_object())

        db.session.add(affair)
        db.session.add(post)
        db.session.commit()
        flash('Your affair has been registered')
        return redirect(url_for('main.index'))
    return render_template('time_manager/register.html', form=form)


@time_manager.route('/usr/<username>/affair')
@login_required
def show_affairs(username):
    user = User.query.filter_by(username=username).one()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for('.index'))
    affairs = user.affairs
    page = request.args.get('page', 1, type=int)
    pagination = user.affairs.paginate(
        page, per_page=current_app.config['FLASKY_AFFAIRS_PER_PAGE'],
        error_out=False)
    return render_template('affair.html', user=user, affairs=affairs, pagination=pagination)
