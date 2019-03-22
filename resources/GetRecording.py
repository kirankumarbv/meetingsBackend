from flask import jsonify, request
from flask_restful import Resource
from Model import db, Recording, RecordingSchema

recordings_schema = RecordingSchema(many=True)


class GetRecordingResource(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data or len(json_data) is not 1 or 'meeting_id' not in json_data:
        	return {'message': 'Input field incorrect'}, 400

        recordings = Recording.query.filter_by(meeting_id=json_data['meeting_id'])
        
        recordings = recordings_schema.dump(recordings).data
        if not recordings:
        	return {'message': 'Input data incorrect or recording does not exist'}, 400

        return {"status":"success", "data":recordings}, 200