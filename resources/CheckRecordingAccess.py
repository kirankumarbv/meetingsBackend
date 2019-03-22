from flask import jsonify, request
from flask_restful import Resource
from Model import db, Recording, ViewRecordingSchema, ViewRecording

view_recordings_schema = ViewRecordingSchema(many=True)
view_recording_schema = ViewRecordingSchema()

class CheckRecordingAccessResource(Resource):

    def post(self):
        json_data = request.get_json(force=True)

        if len(json_data) is not 2 or 'recording_id' not in json_data or 'email_id' not in json_data:
            return {'message': 'Input fields incorrect'}, 400  
        
        view_recording = ViewRecording.query.filter_by(recording_id=json_data['recording_id'], email_id=json_data['email_id']).first()
        if not view_recording:
            return {'status': "failure"}, 400

        return {'status': "success"}, 200