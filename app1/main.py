from flask import Flask, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

oauth = OAuth()
oauth.init_app(app)
oauth.register(
    'gluu',
    server_metadata_url='https://sso.csgov2.online/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid'}
)


@app.route('/')
def homepage():
    user = session.get('user')
    return user


@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return oauth.gluu.authorize_redirect(redirect_uri)


@app.route('/callback')
def callback():
    token = oauth.gluu.authorize_access_token()
    session['user'] = token['userinfo']
    return token


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
