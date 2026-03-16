import sqlite3

conn = sqlite3.connect("university.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Students(
id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Professors(
id INTEGER PRIMARY KEY,
name TEXT,
department TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Courses(
id INTEGER PRIMARY KEY,
course_name TEXT,
professor_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollments(
id INTEGER PRIMARY KEY,
student_id INTEGER,
course_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Grades(
id INTEGER PRIMARY KEY,
student_id INTEGER,
course_id INTEGER,
grade INTEGER
)
""")
students = [
("Aruzhan",20),
("Dias",21),
("Aigerim",19)
]

cursor.executemany("INSERT INTO Students(name,age) VALUES (?,?)", students)

courses = [
("Databases",1),
("Artificial Intelligence", 2)
]

cursor.executemany("INSERT INTO Courses(course_name, professor_id) VALUES (?,?)", courses)

enrollments = [
(1,1),
(2,1),
(3,2)
]

cursor.executemany("INSERT INTO Enrollments(student_id,course_id) VALUES (?,?)", enrollments)

conn.commit()
cursor.execute("SELECT * FROM Students")

print("Барлық студенттер:")
for s in cursor.fetchall():
    print(s)

cursor.execute("""
SELECT Students.name
FROM Students
JOIN Enrollments ON Students.id = Enrollments.student_id
JOIN Courses ON Courses.id = Enrollments.course_id
WHERE Courses.course_name = 'Databases'
""")

print("Databases курсына тіркелген студенттер:")
for s in cursor.fetchall():
    print(s)

cursor.execute("""
INSERT INTO Grades(student_id,course_id,grade)
VALUES(2,1,85)
""")

conn.commit()

cursor.execute("""
SELECT Students.name, Courses.course_name, Grades.grade
FROM Grades
JOIN Students ON Students.id = Grades.student_id
JOIN Courses ON Courses.id = Grades.course_id
WHERE Grades.grade >= 50
""")

print("Курсты аяқтаған студенттер:")
for s in cursor.fetchall():
    print(s)

cursor.execute("""
DELETE FROM Enrollments
WHERE id NOT IN (
    SELECT MIN(id)
    FROM Enrollments
    GROUP BY student_id, course_id
)
""")

conn.commit()

conn.close()
