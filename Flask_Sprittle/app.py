from flask import Flask, render_template, request, redirect, url_for, jsonify,session
import threading
import cv2
import os
from sql_it import sqlsignup  
from sql_it import sqllogin
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'




@app.route('/', methods =["GET", "POST"])
def home():
    return render_template("userauthentication.html")


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       email = request.form.get("email")
       # getting input with name = lname in HTML form
       password = request.form.get("password")
       print(email,password)
       if sqllogin(email,password)=='found':
           return render_template('index.html',videos=videos)  
       elif sqllogin(email,password)=='nouser':
           return redirect(url_for("invaliduser"))         
       elif sqllogin(email,password)=='wrongpass':
           return redirect(url_for("incorrect"))
           
       #return redirect(url_for("home"))
       
       


@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       username = request.form.get("username")
       email = request.form.get("email")
       # getting input with name = lname in HTML form
       password = request.form.get("password")
       print(username,email,password)
       sqlsignup(username,email,password)
           #return redirect(url_for("model"))
       return redirect(url_for("home"))







# User logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# Sample data structure to store videos
videos = [
    {
        'id': 1,
        'name': 'Video 1',
        'path': r'D:\Flask_Sprittle\uploads\Flipgrid English.mp4'
    },
    {
        'id': 2,
        'name': 'Video 2',
        'path': r'D:\Flask_Sprittle\uploads\Flipgrid English.mp4'
    }
]

next_video_id = 3

# Video streaming thread
class VideoThread(threading.Thread):
    def __init__(self, video_path):
        threading.Thread.__init__(self)
        self.video_path = video_path

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Process frame here (e.g., apply filters, resize, etc.)
            # ...
            cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

# Home page
'''@app.route('/')
def index():
    return render_template('index.html')
'''
# User authentication
# You'll need to implement user authentication functionality separately



@app.route('/api/videos', methods=['GET', 'POST'])
def all_videos():
    if request.method == 'GET':
        return jsonify(videos)
    elif request.method == 'POST':
        global next_video_id
        name = request.form['name']
        video_file = request.files['video']
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(video_path)
        video = {'id': next_video_id, 'name': name, 'path': video_path}
        next_video_id += 1
        videos.append(video)
        #return jsonify(video), 201
        return render_template('list.html', videos=videos)
    
    @app.route('/api/videos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def video(id):
        video = next((v for v in videos if v['id'] == id), None)
        if not video:
            return jsonify({'error': 'Video not found'}), 404

        if request.method == 'GET':
            return jsonify(video)
        elif request.method == 'PUT':
            video['name'] = request.form.get('name', video['name'])
            return jsonify(video)
        elif request.method == 'DELETE':
            videos.remove(video)
            return '', 204

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_video(id):
    video = next((v for v in videos if v['id'] == id), None)
    if not video:
        return 'Video not found'

    if request.method == 'GET':
        return render_template('edit.html', video_id=id, video_path=video['path'])
    elif request.method == 'PUT':
        video['path'] = request.form.get('path', video['path'])
        os.rename('path', videos['path'])
        return jsonify(video)


def edit_video(id):
    video = next((v for v in videos if v['id'] == id), None)
    if not video:
        return 'Video not found'

    if request.method == 'POST':
        return render_template('edit.html', video=video)
        video['name'] = request.form.get('name', video['name'])
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form.get('path', ''))
        if os.path.exists(video_path):
            video['path'] = video_path
            return jsonify(video)
        return render_template('edit.html', video=video, message='Video updated successfully')
'''
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_video(id):
    video = next((v for v in videos if v['id'] == id), None)
    if not video:
        return 'Video not found'

    if request.method == 'POST':
        new_path = request.data.decode('utf-8')
        video['name'] = request.form.get('name', video['name'])
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], new_path)
        if os.path.exists(video_path):
            video['path'] = video_path
            return render_template('edit.html', video=video, message='Video updated successfully')
        else:
            return render_template('edit.html', video=video, message='Invalid video path')

    return render_template('edit.html', video=video)

'''

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_video(id):
    video = next((v for v in videos if v['id'] == id), None)
    if not video:
        return 'Video not found'

    if request.method == 'POST':
        video['name'] = request.form.get('name', video['name'])
        new_path = request.form.get('path', video['path'])
        #print(new_path)
        if os.path.exists(new_path):
            # Update video path and move the video file to the new location
            video['path'] = new_path
            new_video_path = os.path.join(new_path, secure_filename(video['name']))
            print(new_video_path)
            print(video['name'])
            shutil.move(video['path'], new_video_path)
            video['path'] = new_video_path
            return render_template('edit.html', video=video, message='Video updated successfully')
        else:
            return render_template('edit.html', video=video, error='Invalid path. Please provide a valid path.')

    return render_template('edit.html', video=video)



@app.route('/api/videos/<int:id>', methods=['DELETE'])
def delete_video(id):
    video = next((v for v in videos if v['id'] == id), None)
    if not video:
        return jsonify({'message': 'Video not found'}), 404

    videos.remove(video)
   # os.remove(video['path'])

    return jsonify({'message': 'Video deleted successfully'})

# Search videos
@app.route('/search', methods=['GET'])
def search_videos():
    query = request.args.get('query', '')
    matching_videos = [video for video in videos if query.lower() in video['name'].lower()]
    print(query)
    return render_template('search_result.html', videos=matching_videos)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port='5000',host="localhost")
    
    
    
    
    
    
    
