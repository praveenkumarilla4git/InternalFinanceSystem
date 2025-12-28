from flask import Flask, render_template  # <--- CHANGE 1: Added render_template

app = Flask(__name__)

@app.route("/")
def home():
    current_user = "Admin User: Praveen"  # <--- created a variable
    print(f"Loading dashboard for: {current_user}") 
    
    # We pass the variable into the template like shipping a package
    return render_template("index.html", user_name=current_user)
    
if __name__ == "__main__":
    app.run(debug=True)