import firebase_admin
import functions_framework
from firebase_admin import credentials, storage, firestore
from season2122 import helper as helper
import io
from flask import jsonify


@functions_framework.http
def handle_request(request):
	"""HTTP Cloud Function.
	Args:
	request (flask.Request): The request object.
		<https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
	Returns:
		The response text, or any set of values that can be turned into a
		Response object using `make_response`
		<https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
	"""
	request_json = request.get_json(silent=True)
	request_args = request.args

	if request_json and 'platform' in request_json:
		platform = request_json['platform']
	elif request_args and 'platform' in request_args:
		platform = request_args['platform']
	else:
		platform = 'facebook'

	if request_json and 'team' in request_json:
		team = request_json['team']
	elif request_args and 'team' in request_args:
		team = request_args['team']
	else:
		team = "1"

	data = create_and_upload(int(team), platform)
	response = jsonify(data)
	response.headers.set('Access-Control-Allow-Origin', '*')
	return response


def create_and_upload(team: int = 1, platform: str = "facebook"):
	if not firebase_admin._apps:
		cred = credentials.Certificate('asv-webservices-firebase-credentials.json')
		firebase_admin.initialize_app(cred, {
			'storageBucket': 'asv-webservices.appspot.com'
		})

	# set document to loading=True
	db = firestore.client()
	doc_ref = db.collection(u'matchday-preview').document(u'{0}_asv{1}'.format(platform, team))
	doc_ref.update({u'loading': True})

	# create image and upload
	img_io = helper.create_image(platform=platform, team=team)
	image_url = upload_image(img_io=img_io, platform=platform, team=team)

	# set document to Loading=False
	doc_ref.update({
		u'loading': False,
		u'imageURL': image_url
	})

	return {"status": "success", "code": 200}


def upload_image(img_io: io.BytesIO = b'', platform: str = "facebook", team: int = 1):
	bucket = storage.bucket()
	blob = bucket.blob(f"{team}_{platform}.png")

	metadata = {'contentType': "image/png"}
	blob.metadata = metadata

	blob.upload_from_string(img_io.getvalue(), content_type='image/png')

	blob.make_public()
	return blob.public_url


if __name__ == "__main__":
	for t in range(1, 3):
		for p in ["facebook", "instagram"]:
			img = helper.create_image(p, t)
			with open(f"{p}_{t}.png", "wb") as f:
				f.write(img.getbuffer())
