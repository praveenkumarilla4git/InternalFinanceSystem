# CHANGE 1: Import 'request'
from flask import Flask, render_template, request 
from core import calculate_savings

app = Flask(__name__)

# CHANGE 2: Allow both GET (viewing) and POST (sending data)
@app.route("/", methods=["GET", "POST"])
def home():
    current_user = "Praveen"
    estimated_annual = None  # Start with nothing
    
    # CHANGE 3: Check if the user just hit the button
    if request.method == "POST":
        # We grab the text from the box named "savings_input"
        user_input = int(request.form["savings_input"]) 
        estimated_annual = calculate_savings(user_input)
    
    return render_template("index.html", user_name=current_user, money=estimated_annual)

if __name__ == "__main__":
    app.run(debug=True)