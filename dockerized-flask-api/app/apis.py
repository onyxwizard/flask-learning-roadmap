# app/api.py
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import request
from . import db
from .models import Entry, User

# Parser for entry data
entry_parser = reqparse.RequestParser()
entry_parser.add_argument('title', required=True)
entry_parser.add_argument('category', required=True)
entry_parser.add_argument('content', required=True)
entry_parser.add_argument('user_id', type=int, required=True)

# API Resources
class ApiLoginResource(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            from flask_jwt_extended import create_access_token
            claims = {"is_admin": user.is_admin}
            access_token = create_access_token(identity=user.username, additional_claims=claims)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid username or password'}, 401


class EntryListResource(Resource):
    @jwt_required()
    def get(self):
        entries = Entry.query.all()
        return [{
            'id': e.id,
            'title': e.title,
            'category': e.category,
            'content': e.content
        } for e in entries]

    @jwt_required()
    def post(self):
        data = entry_parser.parse_args()
        user = User.query.get(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404

        new_entry = Entry(**data)
        db.session.add(new_entry)
        db.session.commit()
        return {'message': 'Entry created', 'id': new_entry.id}, 201


class EntryResource(Resource):
    @jwt_required()
    def get(self, entry_id):
        entry = Entry.query.get_or_404(entry_id)
        return {
            'id': entry.id,
            'title': entry.title,
            'category': entry.category,
            'content': entry.content
        }

    @jwt_required()
    def put(self, entry_id):
        data = entry_parser.parse_args()
        entry = Entry.query.get_or_404(entry_id)
        entry.title = data['title']
        entry.category = data['category']
        entry.content = data['content']
        db.session.commit()
        return {'message': 'Entry updated'}

    @jwt_required()
    def delete(self, entry_id):
        entry = Entry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()
        return {'message': 'Entry deleted'}