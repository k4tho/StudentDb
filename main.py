"""
Creates a student database and allows users to execute commands to interact with it.
Contains a menu of commands that the user will be allowed to run and instructions
on how to execute them.
"""

import sqlite3
import requests
import csv
import json

def create_table():
    """
    Executes an sql command that creates a table.
    """

    mycursor.execute("CREATE TABLE IF NOT EXISTS Student (StudentId INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, GPA REAL, Major TEXT, FacultyAdvisor TEXT, Address TEXT, City TEXT, State TEXT, ZipCode TEXT, MobilePhoneNumber TEXT, isDeleted INTEGER)")
    conn.commit()

def import_data():
    """
    Executes an sql command that imports data into the csv file.
    May need to edit path to csv data file.
    """

    with open('C:\\Users\\katie\\Downloads\\students.csv', 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            mycursor.execute("INSERT INTO Student(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, 0)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],),)
            conn.commit()

def show_menu():
    """
    Prints the menu to display commands to user.
    """

    print()
    print("Menu")
    print("Enter 'q' to exit.")
    print("(1)   Display all students.")
    print("(2)   Add new student.")
    print("(3)   Update student.")
    print("(4)   Delete student.")
    print("(5)   Search for students.")

def process_input(user_input):
    """
    Executes the command based on the user_input in the parameters.
    May require more user input depending on which option was chosen.

    :param user_input: string that represents which command the user chose
    :return: int to indicate that the commands were executed successfully or unsuccessfully
    """

    #Option 1: Display all students
    if user_input == '1':
        display_all_students()
    #Option 2: Add a student
    elif user_input == '2':
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        address = input("Enter address: ")
        city = input("Enter city: ")
        state = input("Enter state: ")
        zip_code = input("Enter zip code: ")
        try:
            int(zip_code)
        except ValueError:
            print("Value entered is not an integer.")
            return
        mobile_phone_number = input("Enter mobile phone number: ")
        try:
            int(mobile_phone_number)
        except ValueError:
            print("Value entered is not an integer.")
            return
        major = input("Enter major: ")
        gpa = input("Enter gpa: ")
        try:
            float(gpa)
        except ValueError:
            print("Value entered is not a float.")
            return
        faculty_advisor = input("Enter faculty advisor: ")
        add_new_student(first_name, last_name, address, city, state, int(zip_code), int(mobile_phone_number), major, float(gpa), faculty_advisor, 0)
        print("New student added.")
    #Option 3: Update student information
    elif user_input == '3':
        student_id = input("Enter student id: ")
        try:
            int(student_id)
        except ValueError:
            print("Value entered is not an integer.")
            return
        identifier = input("Update (1) major, (2) faculty advisor, (3) mobile phone number: ")
        if identifier == '1':
            major = input("Enter major: ")
            update_student(int(student_id), major, None, None)
        elif identifier == '2':
            faculty_advisor = input("Enter faculty advisor: ")
            update_student(int(student_id), None, faculty_advisor, None)
        elif identifier == '3':
            mobile_phone_number = input("Enter mobile phone number: ")
            try:
                int(mobile_phone_number)
            except ValueError:
                print("Value entered is not an integer.")
                return
            update_student(int(student_id), None, None, int(mobile_phone_number))
        else:
            print("Invalid option")
    #Option 4: Delete student
    elif user_input == '4':
        student_id = input("Enter student id: ")
        try:
            int(student_id)
        except ValueError:
            print("Value entered is not an integer.")
            return
        delete_student(student_id)
        print("Student id was deleted.")
    #Option 5: Search study by cateogory
    elif user_input == '5':
        identifier = input("Search student by (1)major, (2)gpa, (3)city, (4)state, (5)faculty advisor: ")
        if identifier == '1':
            major = input("Enter major: ")
            search_students(major, None, None, None, None)
        elif identifier == '2':
            gpa = input("Enter gpa: ")
            try:
                float(gpa)
            except ValueError:
                print("Value entered is not a float.")
                return
            search_students(None, float(gpa), None, None, None)
        elif identifier == '3':
            city = input("Enter city: ")
            search_students(None, None, city, None, None)
        elif identifier == '4':
            state = input("Enter state: ")
            search_students(None, None, None, state, None)
        elif identifier == '5':
            faculty_advisor = input("Enter faculty advisor: ")
            search_students(None, None, None, None, faculty_advisor)
        else:
            print("Invalid option")
    #Returns 1 if the function was unable to execute any of the five options.
    else:
        return 1
    #Returns 0 if the function was able to execute one of five options
    return 0

def display_all_students():
    """
    Executes an sql query to displays all students.
    """

    mycursor.execute("SELECT * FROM Student;")
    conn.commit()

def add_new_student(first_name, last_name, address, city, state, zip_code, mobile_phone_number, major, gpa, faculty_advisor):
    """
    Adds a new student to the table based on the attributes in the parameters.

    :param first_name: string that represents student's first name
    :param last_name: string that represents student's last name
    :param address: string that represents student's street address
    :param city: string that represent student's home city
    :param state: string that represent student's home state
    :param zip_code: int that represents student's home zip code
    :param mobile_phone_number: int that represents student's mobile phone number
    :param major: string that represents student's major
    :param gpa: float that represents student's gpa
    :param faculty_advisor: string that represents student's faculty advisor
    """

    mycursor.execute(
        "INSERT INTO Student(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)",
        (first_name, last_name, address, city, state, zip_code, mobile_phone_number, major, gpa, faculty_advisor,), )
    conn.commit()

def delete_student(student_id):
    """
    Executes an sql query that deletes student from table based on student id.

    :param student_id: int that represents the student's id
    """
    mycursor.execute("DELETE FROM Student WHERE StudentId = " + str(student_id))
    conn.commit()

def update_student(student_id, major, faculty_advisor, mobile_phone_number):
    """
    Executes an sql query that updates a student's major, faculty advisor, or mobile phone number.

    :param student_id: int that represents the student id to find which student to update
    :param major: string that represents the new major that will get updated
    :param faculty_advisor: string that represents the new faculty advisor that will get updated
    :param mobile_phone_number: int that represents the new mobile phone number that will get updated
    :return:
    """

    #Checks for first argument that is not None and updates that field for student.
    if major is not None:
        mycursor.execute("UPDATE Student SET Major = ? WHERE StudentID = ?", (major, student_id))
    if faculty_advisor is not None:
        mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentID = ?", (faculty_advisor, student_id))
    if mobile_phone_number is not None:
        mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentID = ?", (mobile_phone_number, student_id))
    conn.commit()

def search_students(major, gpa, city, state, faculty_advisor):
    """
    Executes an sql query that searches for students based upon the major, gpa, city, state, or faculty advisor.

    :param major: string that represents the student's major
    :param gpa: float that represents the student's gpa
    :param city: string that represents the student's home city
    :param state: string that represents the student's home state
    :param faculty_advisor: string that represents the student's faculty advisor
    """

    # Checks for first argument that is not None and searches for students based on that field.
    if major is not None:
        mycursor.execute("SELECT * from Student WHERE Major = ?", (major,))
    elif gpa is not None:
        mycursor.execute("SELECT * from Student WHERE GPA = ?", (gpa,))
    elif city is not None:
        mycursor.execute("SELECT * from Student WHERE City = ?", (city,))
    elif state is not None:
        mycursor.execute("SELECT * from Student WHERE State = ?", (state,))
    elif faculty_advisor is not None:
        mycursor.execute("SELECT * from Student WHERE FacultyAdvisor = ?", (faculty_advisor,))
    conn.commit()



#Creates a new database and connects the program to it.
conn = sqlite3.connect('Students.db')
mycursor = conn.cursor()

#Creates table in the database and imports data from csv file.
create_table()
import_data()

#Checks if the user has pressed 'q' to exit.
hasExited = False
while (hasExited == False):
    show_menu()
    user_input = input("Which command would you like to execute? ")
    #User has chosen to exit the program.
    if user_input == 'q':
        hasExited = True
    #Checks if the user has selected an option that is not 1-5 or 'q'.
    elif process_input(user_input) == 1:
        print("Invalid option.")
    #Prints out the sql query execution.
    else:
        rows = mycursor.fetchall()
        for row in rows:
            print(row)
