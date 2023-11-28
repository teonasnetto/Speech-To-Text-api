import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, flash, request, redirect, url_for, send_from_directory
from reconhecer_voz import ReconhecerVoz
from converter_audio import ConverterAudio

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'mp3'}

if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024  * 1024
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'uma_chave_secreta_padrão_se_a_variável_não_for_encontrada')
KEY = '456sdfa8vb4'

#habilita o modo de debug do flask
app.config['DEBUG'] = True

def allowed_file(filename:str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.errorhandler(500)
def too_large(e):
    return "Some error", 500

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return files

@app.route('/stt', methods=['GET', 'POST'])
def convert_stt():
	# recebe o arquivo de audio via POST
	if request.method == 'POST':
		# check the token in header
		if request.headers.get('token'):
			token = request.headers.get('token')
			if token != KEY:
				return jsonify({'status': 'error', 'message': 'token invalid'}), 401
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return 'No file part'
		file = request.files['file']
		# If the user does not select a file, the browser submits an
		# empty file without a filename.
		if file.filename == '':
			flash('No selected file')
			return 'No selected file'
		if not allowed_file(file.filename):
			flash('Not Allowed')
			return 'This format is not Allowed '
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			#limpa a pasta tmp
			files = os.listdir(app.config['UPLOAD_FOLDER'])
			for f in files:
				os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
			# salva o arquivo na pasta tmp
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# convert to wav
			audio_name = 'audio.wav'
			conversor = ConverterAudio(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], audio_name))
			conversor.convert_to_wav()
			reconhecer_voz = ReconhecerVoz(os.path.join(app.config['UPLOAD_FOLDER'], audio_name))
			texto = reconhecer_voz.reconhecer()

			return texto
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form method=post enctype=multipart/form-data>
	<input type=file name=file>
	<input type=submit value=Upload>
	</form>
	'''
@app.route('/uploads/<filename>')
def upload(filename):
	return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == '__main__':
	app.run(host='0.0.0.0')