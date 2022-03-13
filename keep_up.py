from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Online"
  
def keep_up():
  app.run(port=80)