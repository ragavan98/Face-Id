from datetime import datetime, timedelta
from flask import g, render_template, request, jsonify, make_response,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_oauthlib.provider import OAuth2Provider
from flask_oauthlib.contrib.oauth2 import bind_sqlalchemy
from flask_oauthlib.contrib.oauth2 import bind_cache_grant
from werkzeug.security import gen_salt
import time
import face
from base64 import b64decode
db = SQLAlchemy()
from flask_cors import CORS
import faceMethods
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True,nullable=False)
    email_id=db.Column(db.String(40),unique=True,nullable=False)
    password = db.Column(db.String(40),unique=True,nullable=False)
    def check_password(self, password):
        return True
class Pics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageFile1=db.Column(db.String(40),nullable=True)
    imageFile2=db.Column(db.String(40),nullable=True)
    imageFile3=db.Column(db.String(40),nullable=True)
    imageFile4=db.Column(db.String(40),nullable=True)
    imageFile5=db.Column(db.String(40),nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    user=db.relationship('User')
    def check_password(self, password):
        return True

class Client(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    client_id = db.Column(db.String(40),nullable=False,unique=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,nullable=False)
    client_uri = db.Column(db.Text)
    _redirect_uris = db.Column(db.Text)
    default_scope = db.Column(db.Text, default='email')
    response_types=db.Column(db.Text)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    user=db.relationship('User')

    @property
    def user(self):
        return User.query.get(1)

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'password', 'client_credentials',
                'refresh_token']


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    client = relationship('Client')
    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    scope = db.Column(db.Text)
    expires = db.Column(db.DateTime)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return None


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id', ondelete='CASCADE'),nullable=False,)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User')
    client = relationship('Client')
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expires = db.Column(db.DateTime)
    scope = db.Column(db.Text)

    def __init__(self, **kwargs):
        expires_in = kwargs.pop('expires_in', None)
        if expires_in is not None:
            self.expires = datetime.utcnow() + timedelta(seconds=expires_in)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None
def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


def cache_provider(app):
    print('cache_provider')
    oauth = OAuth2Provider(app)

    bind_sqlalchemy(oauth, db.session, user=User,
                    token=Token, client=Client)

    app.config.update({'OAUTH2_CACHE_TYPE': 'simple'})
    bind_cache_grant(app, oauth, current_user)
    return oauth


def sqlalchemy_provider(app):
    print('sqlalchemy_provider')
    oauth = OAuth2Provider(app)

    bind_sqlalchemy(oauth, db.session, user=User, token=Token,
                    client=Client, grant=Grant, current_user=current_user)

    return oauth


def default_provider(app):
    print('default_provider')
    oauth = OAuth2Provider(app)

    @oauth.clientgetter
    def get_client(client_id):
        print('get_client')
        return Client.query.filter_by(client_id=client_id).first()

    @oauth.grantgetter
    def get_grant(client_id, code):
        print('get_grant')
        return Grant.query.filter_by(client_id=client_id, code=code).first()

    @oauth.tokengetter
    def get_token(access_token=None, refresh_token=None):
        print('get_token')
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        if refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()
        return None

    @oauth.grantsetter
    def set_grant(client_id, code, request, *args, **kwargs):
        print('set_grant')
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            scope=' '.join(request.scopes),
            user_id=g.user.id,
            expires=expires,
        )
        db.session.add(grant)
        db.session.commit()

    @oauth.tokensetter
    def set_token(token, request, *args, **kwargs):
        print('set_token')
        # In real project, a token is unique bound to user and client.
        # Which means, you don't need to create a token every time.
        tok = Token(**token)
        tok.user_id = request.user.id
        tok.client_id = request.client.client_id
        db.session.add(tok)
        db.session.commit()

    @oauth.usergetter
    def get_user(username, password, *args, **kwargs):
        print('get_user')
        # This is optional, if you don't need password credential
        # there is no need to implement this method
        return User.query.filter_by(username=username).first()

    return oauth


def prepare_app(app):
    print('prepare_app')
    db.init_app(app)
    db.app = app
    db.create_all()
    return app

def base64_to_img(bs4):
    i = bs4.index(",")
    bs4 = bs4[i+1:]
    return b64decode(bs4)

def recognise_people(img):
    file = face.recognise_face(img)
    if file:
        face1 = Pics.query.filter_by(imageFile1=file).first()
        face2 = Pics.query.filter_by(imageFile2=file).first()
        face3 = Pics.query.filter_by(imageFile3=file).first()
        face4 = Pics.query.filter_by(imageFile4=file).first()
        face5 = Pics.query.filter_by(imageFile5=file).first()
        if face1:
            id,imageFile1= face1
            print(id)
            return face1
        if face2:
            id,imageFile1= face2
            print(id)
            return face2
        if face3:
            id,imageFile1= face3
            print(id)
            return face3
        if face4:
            id,imageFile1= face4
            print(id)
            return face4
        if face5:
            id,imageFile1= face5
            print(id)
            return face5
    return False

def storeImages(requestedUserId,image1,image2,image3,image4,image5):
    image_data1=base64_to_img(image1)
    image_data2=base64_to_img(image2)
    image_data3=base64_to_img(image3)
    image_data4=base64_to_img(image4)
    image_data5=base64_to_img(image5)
    PATH="D:\Faces"
    img1=f"{PATH}\\temp_img1.jpg"
    img2=f"{PATH}\\temp_img2.jpg"
    img3=f"{PATH}\\temp_img3.jpg"
    img4=f"{PATH}\\temp_img4.jpg"
    img5=f"{PATH}\\temp_img5.jpg"
    try:
        with open(img1, "x") as f:
                f.close()
    except FileExistsError:
        pass
    with open(img1, "rb+") as f:
        f.write(image_data1)
    try:
        with open(img2, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img2, "rb+") as f:
        f.write(image_data2)
    try:
        with open(img3, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img3, "rb+") as f:
        f.write(image_data3)
    try:
        with open(img4, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img4, "rb+") as f:
        f.write(image_data4)
    try:
        with open(img5, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img5, "rb+") as f:
        f.write(image_data5)
    print("Photo has been written")
    res1=recognise_people(img1)
    res2=recognise_people(img2)
    res3=recognise_people(img3)
    res4=recognise_people(img4)
    res5=recognise_people(img5) 
    if res1:
        username, email_id= res1
        print(username)
        print(username, email_id)
        data = "user Exits"
        return jsonify({'status':data})         
    elif res2:
        username, email_id=res2
        print(username)
        print(username, email_id)
        data = "user Exits"
        return jsonify({'status':data})
    elif res3:
        username, email_id=res3
        print(username)
        print(username, email_id)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res4:
        username, email_id=res4
        print(username)
        print(username, email_id)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res5:
        username, email_id=res5
        print(username)
        print(username, email_id)
        data = "user Exits"
        return jsonify({'status':data}) 
    pics = Pics.query.filter_by(user_id=requestedUserId).first()
    if not pics:
        pics = Pics(imageFile1=img1, imageFile2=img2, imageFile3=img3,imageFile4=img4,user_id=requestedUserId)
        db.session.add(pics)
        db.session.commit()
        session['id'] = requestedUserId
        return True
    return False

def create_server(app, oauth=None):
    print('create_server')
    if not oauth:
        oauth = default_provider(app)

    app = prepare_app(app)

    # @app.route('/requ', methods=('GET', 'POST'))
    # def requ():
    #     if request.method == 'POST':
    #         username = request.form.get('username')
    #         user = User.query.filter_by(username=username).first()
    #         if not user:
    #             return redirect(url_for('requ'))
    #         session['id'] = user.id
    #         # if user is not just to log in, but need to head back to the auth page, then go for it
    #         next_page = request.args.get('next')
    #         if next_page:
    #             return redirect(next_page)
    #         return redirect('/')
    #     user = current_user()
    #     return render_template('requ.html', user=user)

    



    @app.route('/requ',methods=('GET','POST'))
    def requ():
        if request.method == 'POST':
            print('In the req method')
            encValue = request.form.get('encodedInputValue')
            # content = request.get_json()
            # encValue = content['value1']
            val = faceMethods.externalRecogniseMethod(encValue)
            if(val['name']=='fail'):  
                return redirect(url_for('requ'))         
            username = val['name']
            email_id = val['email']
            print(username, email_id)
            user = User.query.filter_by(username=username).first()
            print(user.id)
            session['id'] = user.id            
            next_page = request.args.get('next')
            if next_page:
                print(next_page)
                return redirect(next_page)
            return redirect('/')
        user = current_user()
        return render_template('requ.html', user=user)
    
    # @app.route('/serverSignUp')
    # def sign():
    #     return render_template('serverSignUp.html')

    @app.route('/serverSignUp',methods=('GET', 'POST'))
    def serverSignUp():
        if request.method == 'POST':
            print("in the method")
            error = None
            userName = request.form['username']
            email_id = request.form['email_id']
            password = request.form['password']
            print(userName,email_id,password)
            user = User.query.filter_by(username=userName).first()
            if user:
                error = 'UserName already exists'
                return render_template('serverSignUp.html',error=error) 
            email_idCheck = User.query.filter_by(email_id=email_id).first()
            if email_idCheck:
                error = 'Email already exists'
                return render_template('serverSignUp.html',error=error)
            if userName and email_id and password:
                print("goin to save")
                user = User(username=userName,email_id=email_id,password=password)
                db.session.add(user)
                db.session.commit()
                session['id'] = user.id
                return redirect('/')
            return render_template('serverSignup.html',error=error)
        return render_template('serverSignUp.html')

    # @app.route('/serverSignIn',methods=('GET', 'POST'))
    # def serversignIn():



        
    @app.route('/', methods=('GET', 'POST'))
    def home():
        if request.method == 'POST':
            username = request.form.get('username')
            password=request.form.get('password')
            print(username, password)
            user = User.query.filter_by(username=username).first()
            error = None
            if user:
                if user.password != password:
                    error = "Invalid Credentials"
                    return render_template('home.html',error=error)
                else:    
                    session['id'] = user.id
                    # if user is not just to log in, but need to head back to the auth page, then go for it
                    next_page = request.args.get('next')
                    if next_page:
                        
                        return redirect(next_page)
                    return redirect('/')
            else: 
                error = "Invalid Credentials"
                return render_template('home.html',error=error)        
        user=current_user()
        
        face = []
        if user:
            pics = Pics.query.filter_by(user_id = user.id).first()
            if pics:
                face = pics
                print("printing face")
                print(face.imageFile1)
            else:
                face=[]    
            clients = Client.query.filter_by(user_id=user.id).all()
        else:
            clients = []     
        return render_template('home.html',user=user,clients=clients,face = face)

    



    @app.route('/updatePhoto' ,methods=('GET', 'POST'))
    def updatePhoto():
        if request.method == 'POST':
            content = request.get_json()
            requestedUserId = content['userId']
            print("userId "+str(requestedUserId))
            image1=content['value1']
            image2=content['value2']
            image3=content['value3']
            image4=content['value4']
            image5=content['value5']
            user = User.query.filter_by(id=requestedUserId).first()
            fromexternalMethod = faceMethods.externalStoreMethod(user.username,user.email_id,image1,image2,image3,image4,image5)
            if fromexternalMethod:
                resp = storeImages(requestedUserId,image1,image2,image3,image4,image5)
                session['id'] = requestedUserId
            session['id'] = requestedUserId
            return redirect('/')
        



    






    @app.route('/logout')
    def logout():
        del session['id']
        return redirect('/')


    @app.route('/create_client', methods=('GET', 'POST'))
    def create_client():
        user = current_user()
        if not user:
            return redirect('/')
        if request.method == 'GET':
            return render_template('create_client.html')

        client_id = gen_salt(24)
        user_id=user.id

        form = request.form
       
        # if form['token_endpoint_auth_method'] == 'none':
        #     client_secret = ''
        # else:
        client_secret = gen_salt(48)
        print(form['client_name'],form["client_uri"])
      
        print(form['client_uri']+'/authorized')
        
        _redirect_uris=form['client_uri']+'/authorized'
        client=Client(name=form["client_name"],client_id=client_id,client_uri= form["client_uri"],client_secret=client_secret,_redirect_uris=_redirect_uris,default_scope='email',user_id=user_id)
        db.session.add(client)
        db.session.commit()
        return redirect('/')


    @app.route('/oauth/authorize', methods=['GET', 'POST'])
    @oauth.authorize_handler
    def authorize(*args, **kwargs):
        print('authorize')
        print('load_current_user')
        user = current_user()
        if user:
            g.user = user
        if not user:
             return redirect(url_for('requ', next=request.url))

        # NOTICE: for real project, you need to require login
        if request.method == 'GET':
            # render a page for user to confirm the authorization
            return render_template('allow.html')

        if request.method == 'HEAD':
            print('head')
            # if HEAD is supported properly, request parameters like
            # client_id should be validated the same way as for 'GET'
            response = make_response('', 200)
            response.headers['X-Client-ID'] = kwargs.get('client_id')
            return response
        print('response')
        confirm = request.form.get('confirm', 'no')
        return confirm == 'yes'

    @app.route('/oauth/token', methods=['POST', 'GET'])
    @oauth.token_handler
    def access_token():
        print('access_token')
        return {}

    @app.route('/oauth/revoke', methods=['POST'])
    @oauth.revoke_handler
    def revoke_token():
        print('revoke_token')
        pass

    @app.route('/api/email')
    @oauth.require_oauth('email')
    def email_api():
        oauth = request.oauth
        return jsonify(email=oauth.user.email_id, username=oauth.user.username)

    @app.route('/api/client')
    @oauth.require_oauth()
    def client_api():
        oauth = request.oauth
        return jsonify(client=oauth.client.name)

    @app.route('/api/address/<city>')
    @oauth.require_oauth('address')
    def address_api(city):
        oauth = request.oauth
        return jsonify(address=city, username=oauth.user.username)

    @app.route('/api/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
    @oauth.require_oauth()
    def method_api():
        return jsonify(method=request.method)

    @oauth.invalid_response
    def require_oauth_invalid(req):
        print('require_oauth_invalid')
        return jsonify(message=req.error_message), 401

    return app


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    CORS(app)
    app.debug = True
    app.secret_key = 'development'
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.sqlite'
    })
    app = create_server(app)
    app.run(host='127.0.0.1',port=5000)