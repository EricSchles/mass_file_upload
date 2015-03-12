from flask import request,Flask, redirect, render_template, url_for
import zipfile
import os
from werkzeug import secure_filename
#config vars
UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(["pdf"])

#initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload",methods=["GET",'POST'])
def upload():
    if request.method == "POST":
        uploads = request.files.getlist("file[]")
        zfile = zipfile.ZipFile("test.zip","w")
        for upload in uploads:
            if upload and allowed_file(upload.filename):
                filename = secure_filename(upload.filename)
                upload.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                zfile.write(filename, filename, zipfile.ZIP_DEFLATED)
        zfile.close()
        return render_template("uploaded_file.html",uploads=[elem.filename for elem in uploads],number_of_uploads=len(uploads))
    return render_template("upload.html")

@app.route("/done",methods=["GET","POST"])
def uploaded_file():
    return render_template("uploaded_file.html")

app.run(debug=True)
