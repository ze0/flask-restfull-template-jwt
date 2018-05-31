from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from uuid import uuid4
from API.utils import token_required, admin_required
from API.model import db, User


users = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@users.record
def record_params(setup_state):
    """
    Configure the blueprint with the watsoft parameters
    """
    app = setup_state.app
    users.config = dict([(key, value) for (key, value) in app.config.items()])


@users.route('/')
@token_required
@admin_required
def index():
    qusers = User.query.all()
    output = []

    for user in qusers:
        user_data = dict()
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@users.route('/<public_id>', methods=['GET'])
@token_required
@admin_required
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = dict()
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@users.route('/', methods=['POST'])
@token_required
@admin_required
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@users.route('/<public_id>', methods=['PUT'])
@token_required
@admin_required
def promote_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@users.route('/<public_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})
