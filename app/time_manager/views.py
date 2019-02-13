from . import time_manager
from flask_login import login_required, current_user
from .forms import AffairRegistrationForm
from ..models import Affair
from .. import db
from flask import flash, redirect, url_for, render_template


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
        db.session.add(affair)
        db.session.commit()
        flash('Your affair has been registered')
        return redirect(url_for('main.index'))
    return render_template('time_manager/register.html', form=form)
