from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

@app.route('/')
def index():
    level = request.args.get('level', 1000) 

    cursor.execute("SELECT course_name, day, time, room, level FROM timetable WHERE level = %s", (level,))
    courses = cursor.fetchall()

    cursor.execute("SELECT DISTINCT level FROM timetable")
    levels = [row[0] for row in cursor.fetchall()]
    
    return render_template('index.html', courses=courses, levels=levels, selected_level=level, student_name="Zafar Khidoyatov")

if __name__ == '__main__':
    app.run(debug=True)
