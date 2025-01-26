"""
Converts the xlsx files into csv and populates the database
"""

import pandas as pd
import random

from datetime import (
    date,
    datetime,
    timedelta,
)
from django.db.utils import IntegrityError

from core.models import (
    Student,
    Teacher,
    User,
)
from school.models import (
    Course,
    Department,
)


def parse(xlsx_file_path):
    """
    Converts the file to a list of dictionaries.
    returns a list of rows of the data to use by the writeTable classes
    Returns:
    list: list of dictionaries of {key: column name, value: cell value}
    """

    df = pd.read_excel(
        xlsx_file_path,
        sheet_name="Sheet1",
        header=0,
    )

    dtype = {
        "first_name": str,
        "last_name": str,
        "email": str,
        "password": str,
        "recovery_question": str,
        "recovery_answer": str,
        "age": int,
        "id": str,
        "name": str,
        "level": int,
        "department_id": str,
        "teacher_id": str,
        "created_at": str,
        "start_level": int,
        "current_level": int,
        "matric_no": str,
    }

    defined = df.columns.tolist()
    dtypes = {}
    for key in defined:
        dtypes[key] = dtype[key]
    df.astype(dtypes)

    if "created_at" in df.columns:
        df.rename(columns={"created_at": "created"}, inplace=True)

    list_dict = df.to_dict(orient="records")
    return list_dict


def writeDjangoAdmin():
    """Executes django attributes to create a superuser"""
    database = parse("admins.xlsx")
    logs = "\t=====Admins=====\n"
    for user_data in database:
        try:
            user = User.objects.create_superuser(**user_data)
            user.save()
            logs += f"SuperUser created successfully\n {user}\n"
        except IntegrityError as e:
            logs += f"SuperUser creation failed\n {e.args[1]}\n"
    return logs


def writeDjangoDept():
    """Executes django attributes to create a department"""
    database = parse("departments.xlsx")
    logs = "\t=====Departments=====\n"
    for department in database:
        try:
            dept = Department.objects.create(**department)
            dept.save()
            logs += f"Department created successfully\n {dept}\n"
        except IntegrityError as e:
            logs += f"Department creation failed\n {e.args[1]}\n"
    return logs


def writeDjangoTeach():
    """Executes django attributes to create a teacher"""
    database = parse("teachers.xlsx")
    logs = "\t=====Teachers=====\n"
    for teacher in database:
        try:
            user_data = {
                "first_name": teacher["first_name"],
                "last_name": teacher["last_name"],
                "email": teacher["email"],
                "password": teacher["password"],
                "recovery_question": teacher["recovery_question"],
                "recovery_answer": teacher["recovery_answer"],
            }
            user = User.objects.create(**user_data)
            user.save()
            teacher_data = {
                "id": teacher["id"],
                "created": teacher["created"],
                "user": user,
            }
            teacher = Teacher.objects.create(**teacher_data)
            teacher.save()
            logs += f"Teacher created successfully\n {user}\n"
        except IntegrityError as e:
            logs += f"Teacher creation failed\n {e.args[1]}\n"
    return logs


def writeDjangoCourse():
    """Executes django attributes to create a course"""
    database = parse("courses.xlsx")
    logs = "\t=====Courses=====\n"
    for course in database:
        try:
            dept = Department.objects.get(id=course["department_id"])
            teach = Teacher.objects.get(id=course["teacher_id"])
            course_data = {
                "id": course["id"],
                "created": course["created"],
                "name": course["name"],
                "level": course["level"],
                "department": dept,
                "teacher": teach,
            }
            course = Course.objects.create(**course_data)
            course.save()
            logs += f"Course created successfully\n {course}\n"
        except (Teacher.DoesNotExist, Department.DoesNotExist) as e:
            logs += f"Course creation failed: Missing or incorrect data\n {e.args[1]}\n"
        except IntegrityError as e:
            logs += f"Course creation failed\n {e.args[1]}\n"
    return logs


def writeDjangoStudent():
    """Executes django attributes to create a student"""
    database = parse("students.xlsx")
    logs = "\t=====Students=====\n"
    for student in database:
        random_year = date.today().replace(
            year=date.today().year - student["age"]
        )
        random_day = timedelta(days=random.randint(0, 365))
        dob = random_year - random_day
        try:
            user_data = {
                "first_name": student["first_name"],
                "last_name": student["last_name"],
                "email": student["email"],
                "password": student["password"],
                "recovery_question": student["recovery_question"],
                "recovery_answer": student["recovery_answer"],
            }
            user = User.objects.create(**user_data)
            user.save()
            dept = Department.objects.get(id=student["department_id"])

            student_data = {
                "id": student["id"],
                "created": student["created"],
                # "age": student["age"],
                "start_level": student["start_level"],
                "current_level": student["current_level"],
                "matric_no": student["matric_no"],
                "department": dept,
                "user": user,
                "date_of_birth": dob,
            }
            student = Student.objects.create(**student_data)
            student.save()
            logs += f"Student created successfully\n {user}\n"
        except Department.DoesNotExist as e:
            logs += f"Student creation failed: Missing or incorrect data\n {e.args[1]}\n"
        except IntegrityError as e:
            logs += f"Student creation failed\n {e.args[1]}\n"
    return logs


def generateSQL():
    """Creates the log file to record data sent to the database"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    with open(f"dump_{timestamp}.log", "w") as dump:
        statements = [
            f"\t===== {datetime.now()} =====\n",
            writeDjangoAdmin(),
            writeDjangoDept(),
            writeDjangoTeach(),
            writeDjangoCourse(),
            writeDjangoStudent(),
        ]
        dump.writelines(statements)
    return "OK"


if __name__ == "__main__":
    generateSQL()
