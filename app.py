import os
from flask import Flask, flash, request, redirect, url_for
import urllib
import shutil
from werkzeug.utils import secure_filename
from collections import Counter

import videoProcessing
import revSearch
import imdbFuncs
import awsFuncs

UPLOAD_FOLDER = 'movies'
ALLOWED_EXTENSIONS = {'mp4', "MP4"}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    dirname = ""
    filename = ""
    if request.method == 'POST':
        # check if the post request has the file part
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dirname = os.path.join(app.config['UPLOAD_FOLDER'], filename[:-4])
            os.mkdir(dirname)
            file.save(os.path.join(dirname,  filename))
            shutil.copyfile(os.path.join(dirname,  filename), os.path.join("static", filename))
            return redirect(url_for('display_video',
                                    dirname = dirname, filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>Find Me If You Can</title>
    <style>
    </style>
    </head>
    <body style="background-image: url('static/bg.jpg');background-size:cover;background-repeat:no-repeat;">
    <center style="margin-top:30vh;">
    <div class="card" style="width:70vh;padding:5px;margin-top:30px;margin-bottom:30px;">
    <div class="card-body">
    <br>
    <br>
    <h1>Find Me If You Can</h1>
    <br>
    <br>
    <form method=post enctype=multipart/form-data>
    <h5>Upload A Video</h5>
      <input type=file name=file>
      <input type=submit value=Upload class="btn btn-primary">
    </form>
    <br>
    <br>
    </div>
    </div>
    </center>
    </body>
    </html>
    '''

@app.route('/display', methods=['GET', 'POST'])
def display_video():
    dirname = request.args.get('dirname')
    filename = request.args.get('filename')

    if request.method == 'POST':
        return redirect(url_for('process_file', dirname = dirname, filename=filename))

    return '''
    <!doctype html>
    <html>
    <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>Find Me If You Can</title>
    <style>
    </style>
    </head>
    <body style="background-image: url('static/bg.jpg');background-size:cover;background-repeat:no-repeat;">
    <center style="margin-top:30vh;">
    <div class="card" style="width:70vh;padding:5px;margin-top:30px;margin-bottom:30px;">
    <div class="card-body">
    <br>
    <br>
    <h3>Is this the video you want to search for?</h3>
    <br>
    <iframe style="min-height:auto; width:auto;" src="{}"></iframe>
    <br>
    <br>
    <form method=post enctype=multipart/form-data>
        <input type=submit value=Search class="btn btn-primary">
         </form>
    <br>
    <br>
    </div>
    </div>
    </center>
    </body>
    </html>
    '''.format("static/"+filename)


# A route to handle processing mp4
@app.route('/upload', methods=['GET'])
def process_file():
    dirname = request.args.get('dirname')
    filename = request.args.get('filename')
    videoPath = '/'.join([dirname, filename])

    # audioPath = videoProcessing.getAudio(videoPath)
    # audioText = videoProcessing.getAudioText(audioPath)
    # respText = revSearch.reverseSearchText(audioText)

    # screenText = getTextFromFrame(screenPath)
    # respText2 = reverseSearchText(screenText)

    framePaths = videoProcessing.getFrames(dirname, videoPath)

    celebs = []
    for framePath in framePaths:
        celebs.extend(awsFuncs.getCelebsFromFrame(framePath))

    celebHash = {}
    for celeb in celebs:
        if celeb[0] in celebHash:
            celebHash[celeb[0]] += 1
        else:
            celebHash[celeb[0]] = 1

    print(celebHash)
    celebList = [(key, val) for key, val in celebHash.items()]
    celebList = sorted(celebList, key = lambda x: x[1], reverse = True)
    print(celebList)
    guess2 = imdbFuncs.getGuessesFromCelebs(celebList)

    movieCounter = Counter()
    for guess in guess2:
        movieCounter[guess[0]] += guess[1]

    # for movie in movieCounter.keys():
    #     movieCounter[movie] += respText.count(movie)

    bruteCount = Counter()
    # if len(movieCounter.keys()) == 0:
    #     bruteCount = imdbFuncs.bruteForce(respText)

    if len(bruteCount) > 0:
        movieCounter = bruteCount

    print(movieCounter.most_common())

    if len(movieCounter.most_common(1)) < 1:
        return '''
         <!doctype html>
    <html>
    <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>Find Me If You Can</title>
    <style>
    </style>
    </head>
    <body style="background-image: url('static/bg.jpg');background-size:cover;background-repeat:no-repeat;">
    <center style="margin-top:30vh;">
    <div class="card" style="width:70vh;padding:5px;margin-top:30px;margin-bottom:30px;">
    <div class="card-body">
    <br>
    <br>
    <h3>We couldn't find what you were looking for...</h3>
    <br>
    <br>
    <p>Were the faces of the actors clear enough?<br>Were they audible?</p>
    </div>
    </div>
    </center>
    </body>
    </html>
        '''
    else:
        print('\n\n\n\n\n\n\n\n\n',celebs,'\n\n\n\n\n\n\n\n')
        cr=[]
        for  i in celebs:
            cr.append(i[0])
        cri = set(cr)
        cri1 = list(cri)
        names = ''
        for i in cri1:
            names+=i+'<br>'
        finalGuess = movieCounter.most_common(1)[0][0]
        return '''
         <!doctype html>
    <html>
    <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>Find Me If You Can</title>
    <style>
    </style>
    </head>
    <body style="background-image: url('static/bg.jpg');background-size:cover;background-repeat:no-repeat;">
    <center style="margin-top:30vh;">
    <div class="card" style="width:70vh;padding:5px;margin-top:30px;margin-bottom:30px;">
    <div class="card-body">
    <br>
    <br>
    <h4>The video you uploaded is from:</h4>
    <br>
    <h2 style="color:green">{}</h2>
    <br>
    <h4>The actor(s) in the clip is/are:</h4>
    <br>
    <h2 style="color:green">{}</h2>
    <br>
    <br>
    </div>
    </div>
    </center>
    </body>
    </html>
        '''.format(finalGuess,names)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=3000, debug=True)
