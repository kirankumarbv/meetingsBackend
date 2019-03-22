from flask import jsonify, request
from flask_restful import Resource
from Model import db, ViewRecording, ViewRecordingSchema

view_recordings_schema = ViewRecordingSchema(many=True)
view_recording_schema = ViewRecordingSchema()

class ViewRecordingResource(Resource):

    def get(self):
        '''json_data = request.get_json()
        if not json_data:'''    
        view_recordings = ViewRecording.query.all()
        view_recordings = view_recordings_schema.dump(view_recordings).data

        #if not request.content_length:
        return {"status":"success", "data":view_recordings}, 200