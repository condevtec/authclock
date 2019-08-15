#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
from flask import Flask, jsonify, session, request
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_httpauth import HTTPBasicAuth

import onetimepass

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py", silent=True)
app.wsgi_app = ProxyFix(app.wsgi_app)

totop_auth = HTTPBasicAuth(realm="totp")

@app.route('/auth/totp')
@totop_auth.login_required
def auth_totp():
    return jsonify(
        {
            "auth": session.get("auth"),
            "expire_at": session.get("expire_at"),
            "domain": request.host
        }
    )


@totop_auth.verify_password
def verify_password(username, password):
    if "expire_at" in session:
        if dt.datetime.strptime(session.get("expire_at"), "%Y-%m-%dT%H:%M:%S.%fZ") <= dt.datetime.utcnow():
            session.clear()
            return False
        else:
            return True
    check = onetimepass.valid_totp(password, app.config['TOTP_SECRET'])
    if check:
        session["auth"] = "totp"
        session["expire_at"] = (dt.datetime.utcnow() + dt.timedelta(hours=24)).isoformat() + "Z"
        session["domain"] = request.host
    return check


@totop_auth.error_handler
def unauthorized():
    return jsonify({"error": "unauthorized"})
