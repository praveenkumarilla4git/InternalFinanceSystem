from flask import Flask, render_template, request
from core import calculate_savings
import sqlite3  # <--- NEW SECTION 1: Import the database tool

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    current_user = "Praveen"
    estimated_annual = None
    
    if request.method == "POST":
        user_input = int(request.form["savings_input"])
        estimated_annual = calculate_savings(user_input)
        
        # <--- NEW SECTION 2: Connect to the DB
        # We open the connection to the file we created in Step 8
        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()
        
        # <--- NEW SECTION 3: Write the data (The "INSERT" command)
        # We use '?' as placeholders for the real data
        cursor.execute(
            "INSERT INTO users_data (username, monthly_savings, projected_annual) VALUES (?, ?, ?)",
            (current_user, user_input, estimated_annual)
        )
        
        connection.commit() # Save the changes
        connection.close()  # Close the file
        print("Data successfully saved to finance.db!") 

    return render_template("index.html", user_name=current_user, money=estimated_annual)

if __name__ == "__main__":
    app.run(debug=True)