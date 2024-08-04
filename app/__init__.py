# app/__init__.py
from .config import Config
from .models import db
from .controllers import setup_controllers
from .views import setup_views
from .utils import setup_utils
