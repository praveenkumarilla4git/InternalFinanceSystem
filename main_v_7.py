from flask import Flask, render_template, request, redirect # <--- Added redirect
import sqlite3
from core import calculate_savings

# 1. CREATE THE APP (This must happen before @app.route)
app = Flask(__name__)

# --- HOME PAGE ROUTE ---
@app.route("/", methods=["GET", "POST"])
def home():
    current_user = "Praveen"
    estimated_annual = None
    
    # Connect to DB
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    
    # If "Calculate" button was clicked
    if request.method == "POST":
        user_input = int(request.form["savings_input"])
        estimated_annual = calculate_savings(user_input)
        
        # Save to DB
        cursor.execute(
            "INSERT INTO users_data (username, monthly_savings, projected_annual) VALUES (?, ?, ?)",
            (current_user, user_input, estimated_annual)
        )
        connection.commit()
        print("New data saved.")

    # Always fetch history
    cursor.execute("SELECT * FROM users_data")
    db_data = cursor.fetchall() 
    
    connection.close()

    return render_template("index.html", 
                           user_name=current_user, 
                           money=estimated_annual, 
                           history=db_data)

# --- DELETE ROUTE (Must be after app is created) ---
@app.route("/delete/<int:row_id>")
def delete_item(row_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    
    # Delete the specific row
    cursor.execute("DELETE FROM users_data WHERE id = ?", (row_id,))
    
    connection.commit()
    connection.close()
    
    # Go back to home page
    return redirect("/")

# --- START SERVER ---
if __name__ == "__main__":
    app.run(debug=True)