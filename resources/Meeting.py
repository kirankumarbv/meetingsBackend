from flask import jsonify, request
from flask_restful import Resource
from Model import db, Meeting, MeetingSchema, Recording, User

meetings_schema = MeetingSchema(many=True)
meeting_schema = MeetingSchema()


class MeetingResource(Resource):

    def get(self):
        '''json_data = request.get_json()
        if not json_data:'''    
        meetings = Meeting.query.all()
        meetings = meetings_schema.dump(meetings).data

        #if not request.content_length:
        return {"status":"success", "data":meetings}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = meeting_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422

        host_id = User.query.filter_by(id=data['host_id']).first()
        if not host_id:
            return {'message': 'host ID is not a valid host'}, 400

        meeting = Meeting(
            host_id = data['host_id'],
            )

        db.session.add(meeting)
        db.session.commit()

        result = meeting_schema.dump(meeting).data

        return {'status': "success", 'data': result}, 201

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        if len(json_data) is not 1 or 'id' not in json_data:
            return {'message': 'Input field incorrect'}, 400
        
        meeting = Meeting.query.filter_by(id=json_data['id']).first()
        if not meeting:
            return {'message': 'Input data incorrect or meeting does not exist'}, 400
        db.session.delete(meeting)
        db.session.commit()

        result = meeting_schema.dump(meeting).data

        return { "status": 'Successfully deleted'}, 200
