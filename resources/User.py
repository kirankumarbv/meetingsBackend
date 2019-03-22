from flask import jsonify, request
from flask_restful import Resource
from Model import db, User, UserSchema, Meeting

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UserResource(Resource):

    def get(self):
        '''json_data = request.get_json()
        if not json_data:'''    
        users = User.query.all()
        users = users_schema.dump(users).data

        if not request.content_length:
            return {"status":"success", "data":users}, 200
        json_data = request.get_json()
        if not json_data:
            return {"status":"success", "data":users}, 200
        user = User.query.filter_by(email_id=json_data['email_id']).first()
        user = user_schema.dump(user).data
        if not user:
            return {'message': 'User does not exist'}, 400
        else:
            return {"status": "success", "data":user}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        user = User.query.filter_by(email_id=data['email_id']).first()
        if user:
        	return {'message': 'User already exists'}, 400
        user = User(
            email_id = data['email_id'],
            name = data['name']
            )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data

        return {'status': "success", 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        user = User.query.filter_by(id=data['id']).first()
        if not user:
            return {'message': 'User does not exist'}, 400
        user.name = data['name']
        user.email_id = data['email_id']
        db.session.commit()

        result = user_schema.dump(user).data

        return {'status': "success", 'data': result}, 201

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        
        if len(json_data) is not 2 or 'id' not in json_data or 'email_id' not in json_data:
            return {'message': 'Input fields incorrect'}, 400

        user = User.query.filter_by(id=json_data['id'], email_id=json_data['email_id']).first()
        if not user:
            return {'message': 'Input data incorrect or user does not exist'}, 400

        db.session.delete(user)
        db.session.commit()

        #result = user_schema.dump(user).data
        return { "status": 'Successfully deleted'}, 200
