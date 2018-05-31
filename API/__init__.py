from flask import Flask, request, g, jsonify, make_response
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import jwt

from API.utils import token_required, admin_required

from API.blueprint.users import users
# from ISVP.blueprints.blank import blank


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Setup Flask-Security
    from API.model import db, User
    db.init_app(app)

    @app.before_first_request
    def before_first_request():
        db.create_all()

    @app.before_request
    def before_request():
        """"
        execute before each request
        check if current language exist
        and store session data in global user for later use
        """

        g.version = app.config['VERSION']

        g.host = f"{app.config['HOST']}:{app.config['PORT']}"

    app.register_blueprint(users, url_prefix='/user')

    @app.route('/login')
    def login():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!1"'})

        user = User.query.filter_by(name=auth.username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!2"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                app.config['SECRET_KEY'])
            print(token.decode('UTF-8'))
            return jsonify({'token': token.decode('UTF-8')})

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!3"'})

    @app.route('/')
    def index():
        return jsonify({'message': 'Hello'})

    @app.route('/protected')
    @token_required
    def protected():
        return jsonify({'message': 'protected'})

    @app.route('/populate')
    def populate():
        from uuid import uuid4
        from API.model import User

        try:
            u = User(public_id=str(uuid4()),
                     name='admin',
                     password=generate_password_hash('42', method='sha256'), admin=True)
            db.session.add(u)
            db.session.commit()
        except IntegrityError:
            return jsonify({'status': 'ko', 'message': 'User already exist'}), 403

        return jsonify({'status': 'ok'})

    return app
