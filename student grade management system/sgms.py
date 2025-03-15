from tkinter import *
from db import Database

db = Database(host='localhost', user='root', password='', database='student_db')

def populate_list():
    part_list.delete(0, END)  # Clear Listbox
    for row in db.fetch():
        part_list.insert(END, row)

def add_item():
    db.insert(student_name_var.get(), student_id.get(), student_age.get(),
              grade_java.get(), grade_python.get(), grade_php.get(),
              grade_javascript.get(), grade_react.get(), grade_dsa.get())
    populate_list()  # Refresh the list after adding

def select_item(event):
    try:
        global selected_item
        index = part_list.curselection()
        if index:  # Check if an item is selected
            selected_item = part_list.get(index[0])
            student_entry.delete(0, END)
            student_entry.insert(END, selected_item[1])

            student_id_entry.delete(0, END)
            student_id_entry.insert(END, selected_item[2])

            student_age_entry.delete(0, END)
            student_age_entry.insert(END, selected_item[3])

            grade_java.set(selected_item[4])
            grade_python.set(selected_item[5])
            grade_php.set(selected_item[6])
            grade_javascript.set(selected_item[7])
            grade_react.set(selected_item[8])
            grade_dsa.set(selected_item[9])  # Populate grades

            total_var.set(selected_item[10])
            avg_var.set(selected_item[11])
    except IndexError:
        pass

def remove_item():
    if selected_item:
        db.remove(selected_item[0])  # Assuming the first element is the ID
        populate_list()

def update_item():
    if selected_item:  # Ensure an item is selected
        # Get the new values
        java_grade = grade_java.get()
        python_grade = grade_python.get()
        php_grade = grade_php.get()
        javascript_grade = grade_javascript.get()
        react_grade = grade_react.get()
        dsa_grade = grade_dsa.get()

        # Calculate total and average
        total = java_grade + python_grade + php_grade + javascript_grade + react_grade + dsa_grade
        average = total / 6 if total else 0  # Prevent division by zero

        # Update the database
        db.update(
            selected_item[0],
            student_name_var.get(),
            student_age.get(),
            java_grade,
            python_grade,
            php_grade,
            javascript_grade,
            react_grade,
            dsa_grade
        )

        # Update the sum and average in the GUI
        total_var.set(total)
        avg_var.set(average)
        clear_input()
        populate_list()  # Refresh the list after updating
        
        

def clear_input():
    student_entry.delete(0, END)
    student_id_entry.delete(0, END)
    student_age_entry.delete(0, END)

    # Reset all grade variables to 0
    grade_java.set(0)
    grade_python.set(0)
    grade_php.set(0)
    grade_javascript.set(0)
    grade_react.set(0)
    grade_dsa.set(0)

    total_var.set(0)
    avg_var.set(0)

def select_top():
    top_student = db.top()  # Call the top method without parameters
    if top_student:  # Check if a student is returned
        # Populate the fields with the top student's information
        student_name_var.set(top_student[1])
        student_id.set(top_student[2])
        student_age.set(top_student[3])
        grade_java.set(top_student[4])
        grade_python.set(top_student[5])
        grade_php.set(top_student[6])
        grade_javascript.set(top_student[7])
        grade_react.set(top_student[8])
        grade_dsa.set(top_student[9])
        total_var.set(top_student[10])
        avg_var.set(top_student[11])

app = Tk()

# Student name
student_name_var = StringVar()
student_label = Label(app, text='Student Name', font=('bold', 12), pady=10)
student_label.grid(row=0, column=0, sticky=W)
student_entry = Entry(app, textvariable=student_name_var, font=(14))
student_entry.grid(row=0, column=1)

# Student ID
student_id = IntVar()
student_id_label = Label(app, text='Student ID', font=('bold', 12), pady=10)
student_id_label.grid(row=1, column=0)
student_id_entry = Entry(app, textvariable=student_id, font=(14))
student_id_entry.grid(row=1, column=1)

# Student age
student_age = IntVar()
student_age_label = Label(app, text='Student Age', font=('bold', 12), pady=10)
student_age_label.grid(row=2, column=0)
student_age_entry = Entry(app, textvariable=student_age, font=(14))
student_age_entry.grid(row=2, column=1)

# Courses and Grades
Label(app, text='Courses', font=('bold', 12)).grid(row=3, column=0)

grade_java = DoubleVar()
grade_python = DoubleVar()
grade_php = DoubleVar()
grade_javascript = DoubleVar()
grade_react = DoubleVar()
grade_dsa = DoubleVar()

course_labels = ['Java', 'Python', 'PHP', 'JavaScript', 'React', 'DSA']
course_vars = [grade_java, grade_python, grade_php, grade_javascript, grade_react, grade_dsa]

for i, (course, var) in enumerate(zip(course_labels, course_vars), start=4):
    Label(app, text=course, font=('bold', 12), pady=5).grid(row=i, column=0, sticky=W)
    Entry(app, textvariable=var, font=(14)).grid(row=i, column=1)

# Sum
total_var = DoubleVar()
Label(app, text='Sum:', font=('bold', 12), pady=5).grid(row=10, column=0, sticky=W)
Entry(app, textvariable=total_var, font=(14), state='readonly').grid(row=10, column=1)

# Average
avg_var = DoubleVar()
Label(app, text='Average:', font=('bold', 12)).grid(row=11, column=0, sticky=W)
Entry(app, textvariable=avg_var, font=(14), state='readonly').grid(row=11, column=1, pady=10)

# Listbox
Label(app, text='List of Students with Grades', font=('bold', 12)).grid(row=12, column=1, pady=10)
part_list = Listbox(app, height=15, width=70, border=0)
part_list.grid(row=13, column=0, columnspan=11, rowspan=6, pady=20, padx=20)

# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=14, column=6, sticky='ns')
part_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=part_list.yview)

# Bind select
part_list.bind('<<ListboxSelect>>', select_item)

# Button section
Button(app, text='Add', font=('bold', 12), command=add_item).grid(row=0, column=4, pady=10, padx=40)
Button(app, text='Remove', font=('bold', 12), command=remove_item).grid(row=1, column=4, pady=10, padx=40)
Button(app, text='Update', font=('bold', 12), command=update_item).grid(row=2, column=4, pady=10, padx=40)
Button(app, text='Select Top Student', font=('bold', 12), command=select_top).grid(row=3, column=4, pady=10, padx=40)
Button(app, text='Clear', font=('bold', 12), command=clear_input).grid(row=4, column=4, pady=10, padx=40)
Button(app, text='Refresh', font=('bold', 12), command=populate_list).grid(row=5, column=4, pady=10, padx=40)

app.title('Student Grade Management System')
app.geometry('1200x720')

populate_list()

app.mainloop()