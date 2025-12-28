from flask import Flask, render_template
from core import calculate_savings  # <--- NEW: Importing your tool from core.py

app = Flask(__name__)

@app.route("/")
def home():
    current_user = "Praveen"
    
    # We use the function from core.py here
    my_savings = 5000
    estimated_annual = calculate_savings(my_savings) 
    
    # We pass both the name AND the calculated money to the HTML
    return render_template("index.html", user_name=current_user, money=estimated_annual)

if __name__ == "__main__":
    app.run(debug=True)