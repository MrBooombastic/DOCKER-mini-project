
# University Timetable Mini Project  
A web application to view university course timetables, created using Flask, PostgreSQL, and Docker.

---

## Guides

### 1. Install Docker and Start PostgreSQL in Docker  

I literaly downloaded them from the official installers, not commands in the terminal

POSTGRES:
https://www.postgresql.org/download/ 

DOCKER:
https://www.docker.com/products/docker-desktop/

---

### 2. Set Up the PostgreSQL Database and Tables  

```sql
-- Connect to the PostgreSQL database (inside the container)
psql -U postgres

-- Create the Timetable table
CREATE TABLE Timetable (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255),
    day VARCHAR(50),
    time VARCHAR(50),
    room VARCHAR(50),
    level INT
);

INSERT INTO Timetable (course_name, day, time, room, level) VALUES
('Global Social Problems', 'Tuesday', '6:00 PM', 'FA 2024', 1000),
('Social Engineering and Society', 'Monday', '1:00 PM', 'FA 2024', 2000),
('Introduction to Global Education', 'Wednesday', '2:00 PM', 'FA 2024', 2000),
('Operating Systems', 'Thursday', '5:00 PM', 'FA 2024', 2000),
('Introduction to Literature', 'Friday', '1:00 PM', 'FA 2024', 1000);

---

### 3. Installation 

python -m venv final

pip install -r requirements.txt

pip install psycopg2-binary


```

---

### 4. Create Flask Application  

```python
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

```

---

### 5. HTML Templates for Flask  

#### **`index.html` (Timetable Viewer)**  

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini project of ZAFAR KHIDOYATOV</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1, h2 {
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            border-radius: 20%;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        table, th, td {
            border: 1px solid #00ccff;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        select {
            margin-top: 20px;
            padding: 5px;
        }
        .filter {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>ZAFAR KHIDOYATOV</h1>
    
    <div class="container">
        <h2>Timetable</h2>

        <form method="get" action="/" class="filter">
            <label for="level">Select Level:</label>
            <select name="level" id="level" onchange="this.form.submit()">
                {% for level in levels %}
                    <option value="{{ level }}" {% if level == selected_level %}selected{% endif %}>{{ level }}</option>
                {% endfor %}
            </select>
        </form>

        <table>
            <tr>
                <th>Course Name</th>
                <th>Day</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Level</th>
            </tr>
            {% for course in courses %}
            <tr>
                <td>{{ course[0] }}</td>
                <td>{{ course[1] }}</td>
                <td>{{ course[2] }}</td>
                <td>{{ course[3] }}</td>
                <td>{{ selected_level }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
```

---

### 6. Running the Flask Application  

```bash
docker build -t os_final_project_last .

docker run -p 5001:5000 --env-file .env os_final_project_last

```
