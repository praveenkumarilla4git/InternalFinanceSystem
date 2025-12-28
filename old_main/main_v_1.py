from flask import Flask, render_template  # <--- CHANGE 1: Added render_template

app = Flask(__name__)

@app.route("/")
def home():
    print("User is asking for the dashboard...") 
    return render_template("index.html")  # <--- CHANGE 2: swapped the string for the file
    
if __name__ == "__main__":
    app.run(debug=True)