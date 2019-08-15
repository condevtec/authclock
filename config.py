# -*- coding: utf-8 -*-

import uuid
import os.path

DEBUG = bool(os.getenv("FLASK_DEBUG", False))
TESTING = bool(os.getenv("FLASK_TESTING", False))
ASSETS_DEBUG = bool(os.getenv("FLASK_TESTING", False))

DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_ECHO = False
SECRET_KEY = os.getenv('SECRET_KEY') or uuid.uuid4().hex

TEMPLATES_AUTO_RELOAD = True

TOTP_SECRET = os.getenv("TOTP_SECRET")
