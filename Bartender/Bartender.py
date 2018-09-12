from flask import Flask
app = Flask(__name__)

@app.route('/')
def RootDir():
    print('Called to root directory')