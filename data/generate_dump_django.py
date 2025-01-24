#!/usr/bin/python3
"""
Converts the xlsx files into a useable sql database through csv
table1.xlsx -> table2.csv -> dump.sql <- file.csv <- file.xlsx
"""

import csv
import pandas as pd

# from hashlib import md5
# import uuid
from django.contrib.auth.hashers import make_password


def hasher(password):
    """hashes a string and returns the hashed value"""
    hashed = make_password(password)
    print(hashed)
    return hashed
    # md5_hash = md5()
    # md5_hash.update(string.encode("utf-8"))
    # return md5_hash.hexdigest()


def csv_parse(xlsx_file_path):
    """
    Converts the file to a csv.
    returns a list of rows of the data to use by the writeTable classes
    """

    filename = xlsx_file_path[:-5] + ".csv"

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
    # try:
    #     df[["password", "recovery_answer"]] = df[["password", "recovery_answer"]].map(lambda x: make_password(x))
    #     # df["password"] = df["password"].apply(make_password)
    #     # df["recovery_answer"] = df["recovery_answer"].apply(make_password)
    # except Exception:
    #     pass
    df.to_csv(
        filename, index=False, quoting=csv.QUOTE_NONNUMERIC, quotechar="'"
    )
    list_rows = []

    with open(filename, "r") as file:
        csv_data = csv.reader(file)
        for row in csv_data:
            list_rows.append(row)
    return list_rows


def writeAdmin():
    """Returns the sql statement to insert data to the admins table"""

    prompt = "INSERT INTO `core_user` (id, created, first_name, last_name, \
email, password, recovery_question, recovery_answer, is_active, is_staff, is_superuser) VALUES "
    write_data = csv_parse("admins.xlsx")

    info = ""
    for row in write_data[1:]:
        info += "("
        info += f"{row[0].replace('-', '')},"
        for cell in row[1:]:
            info += cell + ","
        info += "1,1,1),"

    info = info[:-1]
    statement = prompt + info + ";\n"

    return statement


# def writeDept():
#     """Returns the sql statement to insert data to the departments table"""

#     prompt = "INSERT INTO `departments` (id, name, created_at) VALUES "
#     write_data = csv_parse("departments.xlsx")

#     info = ""
#     for row in write_data[1:]:
#         info += "("
#         for cell in row:
#             info += cell + ","
#         info = info[:-1]
#         info += "),"

#     info = info[:-1]
#     statement = prompt + info + ";\n"

#     return statement


# def writeTeach():
#     """Returns the sql statement to insert data to the teachers table"""

#     prompt = "INSERT INTO `teachers` (department_id, id, created_at, \
# first_name, last_name, email, password, recovery_question, \
# recovery_answer) VALUES "
#     write_data = csv_parse("teachers.xlsx")

#     info = ""
#     for row in write_data[1:]:
#         info += "("
#         for cell in row:
#             info += cell + ","
#         info = info[:-1]
#         info += "),"

#     info = info[:-1]
#     statement = prompt + info + ";\n"

#     return statement


# def writeCourse():
#     """Returns the sql statement to insert data to the courses table"""

#     prompt = "INSERT INTO `courses` (name, level, department_id, teacher_id, \
# id, created_at) VALUES "
#     write_data = csv_parse("courses.xlsx")

#     info = ""
#     for row in write_data[1:]:
#         info += "("
#         for cell in row:
#             info += cell + ","
#         info = info[:-1]
#         info += "),"

#     info = info[:-1]
#     statement = prompt + info + ";\n"

#     return statement


# def writeStudent():
#     """Returns the sql statement to insert data to the students table"""

#     prompt = "INSERT INTO `students` (age, start_level, current_level, \
# matric_no, department_id, id, created_at, first_name, last_name, email, \
# password, recovery_question, recovery_answer) VALUES "
#     write_data = csv_parse("students.xlsx")

#     info = ""
#     for row in write_data[1:]:
#         info += "("
#         for cell in row:
#             info += cell + ","
#         info = info[:-1]
#         info += "),"

#     info = info[:-1]
#     statement = prompt + info + ";\n"

#     return statement


def generateSQL():
    """Creates the sql file to insert sql statements to the database"""
    with open("dump.sql", "w") as dump:
        statements = [
            "USE schub;\n",
            writeAdmin(),
            # writeDept(),
            # writeTeach(),
            # writeCourse(),
            # writeStudent(),
        ]

        dump.writelines(statements)
        return "OK"


if __name__ == "__main__":
    generateSQL()
