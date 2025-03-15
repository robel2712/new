import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
   
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cur = self.conn.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            student_name TEXT NOT NULL,
            student_id INT NOT NULL,
            student_age INT CHECK(student_age BETWEEN 0 AND 100),
            java_grade FLOAT CHECK(java_grade BETWEEN 0 AND 100),
            python_grade FLOAT CHECK(python_grade BETWEEN 0 AND 100),
            php_grade FLOAT CHECK(php_grade BETWEEN 0 AND 100),
            javascript_grade FLOAT CHECK(javascript_grade BETWEEN 0 AND 100),
            react_grade FLOAT CHECK(react_grade BETWEEN 0 AND 100),
            dsa_grade FLOAT CHECK(dsa_grade BETWEEN 0 AND 100),
            total FLOAT,
            average FLOAT 
        )''')
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return rows
    def insert(self, student_name, student_id, student_age, java_grade, python_grade, php_grade, javascript_grade, react_grade, dsa_grade):
        total = java_grade + python_grade + php_grade + javascript_grade + react_grade + dsa_grade
        average = total / 6
        self.cur.execute(
            "INSERT INTO students (student_name, student_id, student_age, java_grade, python_grade, php_grade, javascript_grade, react_grade, dsa_grade, total, average) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (student_name, student_id, student_age, java_grade, python_grade, php_grade, javascript_grade, react_grade, dsa_grade, total, average)
        )
        self.conn.commit()

    def remove(self, student_id):
        self.cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        self.conn.commit()

    def update(self, student_id, student_name, student_age, java_grade, python_grade, php_grade, javascript_grade, react_grade, dsa_grade):
        total = java_grade + python_grade + php_grade + javascript_grade + react_grade + dsa_grade
        average = total / 6 if total else 0  # Prevent division by zero

        self.cur.execute(
            "UPDATE students SET student_name = %s, student_age = %s, java_grade = %s, python_grade = %s, php_grade = %s, javascript_grade = %s, react_grade = %s, dsa_grade = %s, total = %s, average = %s WHERE id = %s",
            (student_name, student_age, java_grade, python_grade, php_grade, javascript_grade, react_grade, dsa_grade, total, average, student_id)  # Use student_id correctly
        )
        self.conn.commit()

    def top(self):
        self.cur.execute("SELECT * FROM students ORDER BY total DESC LIMIT 1")
        return self.cur.fetchone()

    def __del__(self):
        if hasattr(self, 'conn'):  # Prevents AttributeError
            self.conn.close()

#  Connect to MySQL (Make sure `student_db` exists)
db = Database(host='localhost', user='root', password='', database='student_db')


