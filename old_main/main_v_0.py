from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("User accessed the homepage") 
    return "Internal Finance System is Live!"

if __name__ == "__main__":
    app.run(debug=True)