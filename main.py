import functions_framework
import firebase_admin
from firebase_admin import credentials, storage, firestore


@functions_framework.http
def hello_http(request):
	"""HTTP Cloud Function.
	Args:
	request (flask.Request): The request object.
		<https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
	Returns:
		The response text, or any set of values that can be turned into a
		Response object using `make_response`
		<https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
	"""
	"""
	request_json = request.get_json(silent=True)
	request_args = request.args

	if request_json and 'name' in request_json:
		name = request_json['name']
	elif request_args and 'name' in request_args:
		name = request_args['name']
	else:
		name = 'World'
	return 'Hello {}!'.format(name)
	"""
	if not firebase_admin._apps:
		cred = credentials.Certificate('asv-webservices-firebase-credentials.json')
		default_app = firebase_admin.initialize_app(cred, {
			'storageBucket': "asv-webservices.appspot.com"
		})

	db = firestore.client()

	with open('img.png', 'rb') as f:
		doc_ref = db.collection(u'matchday-preview').document(u'6jEocVGmJ2YJbOw07onY')
		doc_ref.update({
			u'loading': True
		})
		file_name = "img.png"
		bucket = storage.bucket()
		blob = bucket.blob(file_name)
		blob.upload_from_filename(file_name)
		storage.bucket().blob('img.png').upload_from_file(file_obj=f)

		# Opt : if you want to make public access from the URL
		blob.make_public()

		print("your file url", blob.public_url)
		doc_ref.update({
			u'imageURL': blob.public_url,
			u'loading': False
		})
	return "Done"
