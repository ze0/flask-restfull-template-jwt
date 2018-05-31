from functools import wraps
from flask import request, jsonify, current_app, g
import jwt

from API.model import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid!'}), 401
        g.current_user = current_user
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()

            if current_user.admin:
                return f(*args, **kwargs)
            else:
                return jsonify({'message': 'Invalid permission.'}), 401
        except jwt.exceptions.DecodeError:
            import sys
            print(sys.exc_info())
            return jsonify({'message': 'What are you dooing here ?'}), 401
    return decorated
