from flask import Flask, render_template,request,flash
from flask import redirect
import re
from datetime import datetime
from datetime import date
import sqlite3

import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app=Flask(__name__)
app.secret_key = "health_prediction_secret"
@app.route('/')
def home():
    return render_template('index.html',today=date.today().isoformat())

#Read Patient Data
@app.route('/patients')
def patients():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    records = cursor.fetchall()
    conn.close()
    return render_template(
        'patients.html',
        patients=records
    )

#Create operation
@app.route('/save',methods=['POST'])
def save():
    Full_name=request.form['Full_name']
    dob=request.form['dob']
    email=request.form['email']

    Glucose = request.form['Glucose']
    Haemoglobin = request.form['Haemoglobin']
    Cholesterol = request.form['Cholesterol']

    #EMAIL VALIDATION
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_pattern, email):
        flash("Invalid Email Address", "error")
        return redirect('/')

    #DOB VALIDATION
    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()

    if dob_date > datetime.today().date():
        flash("Date of Birth cannot be in the future", "error")
        return redirect('/')
    
    #Numeric Validation
    try:
        Glucose = float(request.form['Glucose'])
        Haemoglobin = float(request.form['Haemoglobin'])
        Cholesterol = float(request.form['Cholesterol'])
    except ValueError:
        flash("Blood test values must be numeric", "error")
        return redirect('/')
    
    # Gemini AI Prediction
    prompt = f"""
    You are a healthcare assistant.

    Patient Blood Test Results:

    Glucose: {Glucose}
    Haemoglobin: {Haemoglobin}
    Cholesterol: {Cholesterol}

    Predict a possible health condition or disease risk.

    Return exactly in this format:

    Possible Disease: <disease/risk>
    Risk Status: <Low Risk / Moderate Risk / High Risk>
    Recommendation: <short recommendation>
    """

    try:
        response = model.generate_content(prompt)
        remarks = response.text
        risk_status = "Unknown"
        for line in remarks.split("\n"):
            if line.startswith("Risk Status:"):
                risk_status = line.replace("Risk Status:", "").strip()
                break
        
    except Exception as e:
        print("Gemini Error:", e)
        remarks = f"AI Error: {str(e)}"
    

    conn=sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute(""" Insert into patients (Full_name,dob,email,Glucose,Haemoglobin,Cholesterol,remarks)
                    values (?,?,?,?,?,?,?)""",
                    (Full_name,dob,email,Glucose,Haemoglobin,Cholesterol,remarks))
    conn.commit()
    conn.close()
    return redirect('/patients')

#Update Operation
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    conn=sqlite3.connect('database.db')
    cursor=conn.cursor()
    if request.method=='POST':
        Full_name=request.form['Full_name']
        dob=request.form['dob']
        email=request.form['email']
        Glucose = request.form['Glucose']
        Haemoglobin = request.form['Haemoglobin']
        Cholesterol = request.form['Cholesterol']
    
        cursor.execute("""
                   UPDATE Patients 
                   SET Full_name=?,
                   dob=?,
                   email=?,
                   Glucose=?,
                   Haemoglobin=?,
                   Cholesterol=?
                   WHERE id=?
                   """,
                   (
                    Full_name,
                    dob,
                    email,
                    Glucose,
                    Haemoglobin,
                    Cholesterol,
                    id
                   ))
        conn.commit()
        conn.close()
        return redirect('/patients')
    cursor.execute("SELECT * FROM patients WHERE id=?",(id,))

    patient = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_patient.html',
        patient=patient
    )
#Delete Operation
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/patients')


if __name__=='__main__':
    app.run(debug=True)



    
