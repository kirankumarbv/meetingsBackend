from flask import Blueprint
from flask_restful import Api
from resources.User import UserResource
from resources.Recording import RecordingResource
from resources.Meeting import MeetingResource
from resources.ViewRecording import ViewRecordingResource
from resources.Share import ShareResource
from resources.GetRecording import GetRecordingResource
from resources.CheckRecordingAccess import CheckRecordingAccessResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(UserResource, '/User')
api.add_resource(MeetingResource, '/Meeting')
api.add_resource(RecordingResource, '/Recording')
api.add_resource(GetRecordingResource, '/GetRecordingsFromMeeting')
api.add_resource(ShareResource, '/ShareRecording')
api.add_resource(ViewRecordingResource, '/ViewRecording')
api.add_resource(CheckRecordingAccessResource, '/CanAccessRecording')