from flask import Blueprint

time_manager = Blueprint('time_manager',__name__)

from . import views