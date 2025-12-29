from flask import Flask, render_template, request, redirect
import sqlite3
from core import calculate_savings

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    current_user = "Praveen"
    estimated_annual = None
    reason_text = None # New variable
    
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    
    if request.method == "POST":
        user_input = int(request.form["savings_input"])
        # UPDATE 1: Get the reason text from HTML
        reason_text = request.form["reason_input"]
        
        estimated_annual = calculate_savings(user_input)
        
        # UPDATE 2: Save the reason to the database
        cursor.execute(
            "INSERT INTO users_data (username, monthly_savings, projected_annual, reason) VALUES (?, ?, ?, ?)",
            (current_user, user_input, estimated_annual, reason_text)
        )
        connection.commit()

    cursor.execute("SELECT * FROM users_data")
    db_data = cursor.fetchall() 
    
    connection.close()

    # UPDATE 3: Pass 'reason' to the template
    return render_template("index.html", 
                           user_name=current_user, 
                           money=estimated_annual, 
                           reason=reason_text,
                           history=db_data)

@app.route("/delete/<int:row_id>")
def delete_item(row_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users_data WHERE id = ?", (row_id,))
    connection.commit()
    connection.close()
    return redirect("/")

if __name__ == "__main__":
    # Ensure this part is exactly as shown:
    app.run(debug=True, host="0.0.0.0")