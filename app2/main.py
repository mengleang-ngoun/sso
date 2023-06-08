from flask import Flask, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

oauth = OAuth()
oauth.init_app(app)
oauth.register(
    'gluu',
    server_metadata_url='https://sso.csgov2.online/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid user_name view_national_id_card'}
)


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route("/userinfo")
def userinfo():
    token = session['token']
    resp = oauth.gluu.get(
        "https://sso.csgov2.online/oxauth/restv1/userinfo", token=token)
    resp.raise_for_status()
    profile = resp.json()
    session["user"] = profile
    return redirect("/")


@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return oauth.gluu.authorize_redirect(redirect_uri)


@app.route('/callback')
def callback():
    token = oauth.gluu.authorize_access_token()
    session['user'] = token['userinfo']
    session['token'] = token
    return redirect("/userinfo")


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
