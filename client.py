from flask import Flask, redirect, url_for, session, request, jsonify, abort,render_template
from flask_oauthlib.client import OAuth


def create_client(app):
    oauth = OAuth(app)
    remote = oauth.remote_app(
        'Face-Id',
        consumer_key='wc4h69PoVaY1MXMEjXgdJzxW',
        consumer_secret='ZyGrykI4ubuCOviH9ZRWvmljE28fXopLxVulFn4Vx4CpwQkI',
        # consumer_key='f2vp1P5ZxYM7UM9xq2jja06I',        
        # consumer_secret='v3fODX0xAHiQjXASN2FyVrSkcTC5KKnZwxgrctIu06K913hY',
        request_token_params={'scope': 'email'},
        base_url='http://127.0.0.1:5000/api/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='http://127.0.0.1:5000/oauth/token',
        authorize_url='http://127.0.0.1:5000/oauth/authorize'
    )

    @app.route('/')
    def index():
        print('index')
        if 'dev_token' in session:
            ret = remote.get('email')
            return jsonify(ret.data)
        return redirect(url_for('login'))
    @app.route('/home')
    def clientHome():
        return render_template('index.html')
    @app.route('/login')
    def login():
        print('login')
        return remote.authorize(callback=url_for('authorized', _external=True))

    @app.route('/logout')
    def logout():
        session.pop('dev_token', None)
        return redirect(url_for('index'))

    @app.route('/authorized')
    def authorized():
        print('authorized')
        resp = remote.authorized_response()
        if resp is None:
            return 'Access denied: error=%s' % (
                request.args['error']
            )
        if isinstance(resp, dict) and 'access_token' in resp:
            session['dev_token'] = (resp['access_token'], '')
            print(resp)
            return redirect('/')
            return jsonify(resp)
        #return redirect('index')    
        return str(resp)

    @app.route('/client')
    def client_method():
        print('client_method')
        ret = remote.get("client")
        if ret.status not in (200, 201):
            return abort(ret.status)
        return ret.raw_data

    @app.route('/address')
    def address():
        print('address')
        ret = remote.get('address/hangzhou')
        if ret.status not in (200, 201):
            return ret.raw_data, ret.status
        return ret.raw_data

    @app.route('/method/<name>')
    def method(name):
        print('method',name)
        func = getattr(remote, name)
        ret = func('method')
        return ret.raw_data

    @remote.tokengetter
    def get_oauth_token():
        print('get_oauth_token')
        return session.get('dev_token')

    return remote


if __name__ == '__main__':
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    # DEBUG=1 python oauth2_client.py
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'development'
    create_client(app)
    app.run(host='localhost', port=8000)