from flask import Flask, render_template, request
import sqlite3
from core import calculate_savings

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    current_user = "Praveen"
    estimated_annual = None
    
    # 1. Open the Connection to the Database
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    
    # 2. IF the user submitted data (clicked Calculate)
    if request.method == "POST":
        # Get the number from the form
        user_input = int(request.form["savings_input"])
        
        # Calculate the result using core.py
        estimated_annual = calculate_savings(user_input)
        
        # Save to Database
        cursor.execute(
            "INSERT INTO users_data (username, monthly_savings, projected_annual) VALUES (?, ?, ?)",
            (current_user, user_input, estimated_annual)
        )
        connection.commit() # Save the file changes
        print("New data saved to database.")

    # 3. ALWAYS: Fetch all past history to display
    cursor.execute("SELECT * FROM users_data")
    db_data = cursor.fetchall() 
    
    # Close the connection so other apps can use the file if needed
    connection.close()

    # 4. Send everything to HTML
    return render_template("index.html", 
                           user_name=current_user, 
                           money=estimated_annual, 
                           history=db_data)

if __name__ == "__main__":
    app.run(debug=True)