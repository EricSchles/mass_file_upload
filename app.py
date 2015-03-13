from flask import request,Flask, redirect, render_template, url_for, send_from_directory, make_response, send_file
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
        return redirect(url_for("download"))
        #return render_template("uploaded_file.html",uploads=[elem.filename for elem in uploads],number_of_uploads=len(uploads))
    return render_template("upload.html")

@app.route("/download",methods=["GET","POST"])
def download():
    filename = "test.zip"
    zfilename = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    return send_file(zfilename)

@app.route("/done",methods=["GET","POST"])
def uploaded_file():
    return render_template("uploaded_file.html")

app.run(debug=True)
