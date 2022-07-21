import os
import time
import shutil
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import mysql_conn


# final upload directory
UPLOAD_FOLDER = './uploads'

# temporary upload directory
TEMP_FOLDER = './temp'

# allowed extensions
ALLOWED_EXTENSIONS = ['mp4', 'mkv']

# initializing the flask app
app = Flask(__name__)

# setting super key for the app
app.secret_key = 'super secret key'

# connecting to the database
mysql = mysql_conn.config_app(app)


# return true if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


# returns length and filename of the video
def get_video_length(file):
    import cv2

    filename = secure_filename(file.filename) # securing the file name

    # filename = filename.split('.')

    #  adding the timestamp to the file name to avoid overwriting
    filename  = f"{int(time.time())}-{filename}"

    # saving the file to the temp folder
    file.save(os.path.join(TEMP_FOLDER, filename))

    # opening the video file in cv2
    video = cv2.VideoCapture(os.path.join(TEMP_FOLDER, filename))

    # getting the fps of the video
    fps = video.get(cv2.CAP_PROP_FPS)

    # getting the total number of frames in the video
    frame  = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # calculating the length of the video in seconds
    length = int(frame / fps)


    return length, filename


# returns the cost of the video
def get_cost(length, size):
    cost  = 5 if size <= (500*1024*1024) else 12.5
    cost += 12.5 if length <= (6*60 + 18) else 20
    return cost


# checks if the file is valid
def validation(file):
    if not allowed_file (file.filename):
        return {"response":False, "message": "Invalid file type"} # invalid file type
    
    file.size = request.content_length  # getting the size of the file
    
    if file.size > 1024**3: # if the file is greater than 1GB 
        return {"response":False, "message": "File size is too large", "size": file.size}
    
    # getting the length of the video
    length, filename = get_video_length(file)

    if length > (10*60):
        os.remove(os.path.join(TEMP_FOLDER, filename))
        return {"response":False, "message": "Video is too long", "length": length}
    
    return {"response":True, "message": "File is valid", "length": length, "filename": filename, "size": file.size}


# endpoint to upload the video
@app.route('/upload', methods=['POST'])
def upload_file():
    file =  request.files['file']
        
    # checking if the file is selected or not
    if file.filename == '':
        return {"response":False, "message": "No file selected"}  # no file selected


    # checking if the file is valid
    validation_result = validation(file)

    if validation_result["response"]==False:  # if the file is invalid
        return validation_result
    
    # moves the valid file to the upload folder
    shutil.move(os.path.join(TEMP_FOLDER, validation_result["filename"]),
                    os.path.join(UPLOAD_FOLDER, validation_result["filename"]))
    
    # computes the cost of the video
    cost = get_cost(validation_result["length"], validation_result["size"])
        
    # inserting the video into the database
    mysql_conn.insert_video(mysql, validation_result["filename"], validation_result["length"], validation_result["size"], cost)
    return {"response" : True,
            "message":"sucess uploading video", 
            "name" : validation_result["filename"],
            "size" : validation_result["size"],
            "length" : validation_result["length"],
            "cost" : cost}
   

# endpoint to get the video cost
@app.route('/getCost', methods=['POST'])
def get_cost_of_video():
    file =  request.files['file']
        
    # checking if the file is selected or not
    if file.filename == '':
        return {"response":False, "message": "No file selected"}
    
    # checking if the file is valid
    validation_result = validation(file)

    if validation_result["response"]==False:  # if the file is invalid
        return validation_result
    os.remove(os.path.join(TEMP_FOLDER, validation_result["filename"]))
    
    # computes the cost of the video
    cost = get_cost(validation_result["length"], validation_result["size"])

    return {"response" : True,
            "message":"Cost of video",
            "cost" : cost}
    

# endpoint to get the videos
@app.route('/getVideos', methods=["GET", "POST"])
def get_videos():
    # if get request then return the all videos
    if request.method == "GET":
        data =  mysql_conn.query_videos(mysql)
        return data

    # if post request then return the videos based on the filter
    elif request.method == "POST":

        # getting the filter from the form
        if request.form != {}:
            data = request.form 
        # getting the filter from the json
        elif request.json != {}:
            data = request.json
        else:
            return {"response":False, "message": "No data received"}

        # getting the videos info based on the filter
        data = mysql_conn.query_videos_filter(mysql, data)
        return data
        
    
# endpoint to home page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
