from flask import jsonify, request
from flask_restful import Resource
from Model import db, Recording, RecordingSchema, Meeting, User, ViewRecording, ViewRecordingSchema

recordings_schema = RecordingSchema(many=True)
recording_schema = RecordingSchema()
view_recording_schema = ViewRecordingSchema()


class RecordingResource(Resource):

    def get(self):
        '''json_data = request.get_json()
        if not json_data:'''    
        recordings = Recording.query.all()
        recordings = recordings_schema.dump(recordings).data

        #if not request.content_length:
        return {"status":"success", "data":recordings}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = recording_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        recording = Recording.query.filter_by(url=data['url']).first()
        if recording:
        	return {'message': 'Recording already exists'}, 400

        if not data['meeting_id']:
            return {'message': 'Meeting ID required'}, 400


        meeting = Meeting.query.filter_by(id=data['meeting_id']).first()
        if not meeting:
            return {'message': 'Meeting Id not valid'}, 400

        private = True if not 'private' in data else data['private']
        md5_hash = None if not 'md5_hash' in data else data['md5_hash']
        length = None if not 'length' in data else data['length']
        recording = Recording(
            url = data['url'],
            meeting_id = data['meeting_id'],
            private = private,
            md5_hash = md5_hash,
            length = length
            )


        db.session.add(recording)
        db.session.commit()

        result = recording_schema.dump(recording).data

        user = User.query.filter_by(id=meeting.host_id).first()

        view_recording = ViewRecording(
            email_id = user.email_id,
            recording_id = result['id']
            )

        db.session.add(view_recording)
        db.session.commit()
        #data, errors = view_recording_schema.load()


        return {'status': "success", 'data': result}, 201

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        
        if len(json_data) is not 1 or 'recording_id' not in json_data:
            return {'message': 'Input field incorrect'}, 400
        recording = Recording.query.filter_by(id=json_data['recording_id']).first()
        if not recording:
            return {'message': 'Input data incorrect or recording does not exist'}, 400
        db.session.delete(recording)
        db.session.commit()

        result = recording_schema.dump(recording).data

        # always returns null even if there is no entry that was deleted
        return { "status": 'Successfully deleted'}, 200

'''    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = recording_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        recording = Recording.query.filter_by(id=data['id']).first()
        if not recording:
            return {'message': 'Recording does not exist'}, 400

        recording.url = data['url']
        recording.length = data['length'] 
        recording.md5_hash = data['md5_hash']
        db.session.commit()

        result = recording_schema.dump(recording).data

        return {'status': "success", 'data': result}, 201'''
