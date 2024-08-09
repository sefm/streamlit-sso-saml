# app.py

import streamlit as st
from flask import Flask, request, redirect, make_response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from saml2.client import Saml2Client
from saml2.response import AuthnResponse
from saml_config import get_saml_config

app = Flask(__name__)
saml_client = Saml2Client(config=get_saml_config())

@app.route('/saml/acs', methods=['POST'])
def saml_acs():
    authn_response = saml_client.parse_authn_request_response(
        request.form['SAMLResponse'],
        entity.BINDING_HTTP_POST
    )
    session_info = authn_response.session_info()
    username = session_info['ava']['uid'][0]
    response = make_response(redirect('/'))
    response.set_cookie('username', username)
    return response

@app.route('/saml/login')
def saml_login():
    _, info = saml_client.prepare_for_authenticate()
    redirect_url = next(iter(info['headers'])[1])
    return redirect(redirect_url)

@app.route('/')
def index():
    username = request.cookies.get('username')
    if not username:
        return redirect('/saml/login')
    return f"Hello, {username}!"

app = DispatcherMiddleware(app, {'/': app})

if __name__ == '__main__':
    st._is_running_with_streamlit = False
    app.run(port=8501)
