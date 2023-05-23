from flask import Flask, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session
from authlib.jose import jwt
from OpenSSL import SSL

app = Flask(__name__)
app.config.from_object('config')

context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_privatekey_file('key.pem')
context.use_certificate_file('cert.pem')   

oauth = OAuth()
oauth.init_app(app)
oauth.register(
    'gluu',
    server_metadata_url='https://localhost/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid'}
)

@app.route("/")
def hello_world():
    args = request.args
    return args

@app.route("/callback")
def callback():
    args = request.args
    return args

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.gluu.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.gluu.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, ssl_context=context)
