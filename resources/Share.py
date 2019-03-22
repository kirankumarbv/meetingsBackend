from flask import jsonify, request
from flask_restful import Resource
from Model import db, Recording, ViewRecordingSchema, ViewRecording

view_recordings_schema = ViewRecordingSchema(many=True)
view_recording_schema = ViewRecordingSchema()

class ShareResource(Resource):

    def post(self):
        json_data = request.get_json(force=True)   
        
        if not json_data or len(json_data) is not 2 or 'recording_id' not in json_data or 'email_id' not in json_data:
            return {'message': 'Input parameters incorrect'}, 400

        recording = Recording.query.filter_by(id=json_data['recording_id']).first()
        if not recording:
            return {'message': 'Recording not found'}, 400

        if recording.private:
            return {'message': 'Recording is private'}, 400

        viewer = ViewRecording.query.filter_by(email_id=json_data['email_id']).first()
        if viewer:
            return {'message': 'Already shared with user'}, 400

        view_recording = ViewRecording(
            email_id = json_data['email_id'],
            recording_id = json_data['recording_id']
            )

        db.session.add(view_recording)
        db.session.commit()

        result = view_recording_schema.dump(view_recording).data

        return {'status': "success", 'data': result}, 200