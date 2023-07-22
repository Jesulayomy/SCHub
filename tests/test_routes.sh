#!/usr/bin/bash

echo -e "API status and stats"
curl http://0:5000/api/status
curl http://0:5000/api/stats

echo -e "\n\n\nroutes"
curl http://0:5000/api/admins/53af4926-52ee-41d0-9acc-ae7230000001

# Department
curl http://0:5000/api/departments/53af4926-52ee-41d0-9acc-ae7230300025
curl http://0:5000/api/departments/53af4926-52ee-41d0-9acc-ae7230300025/courses

# Student
curl http://0:5000/api/students/53af4926-52ee-41d0-9acc-ae7230209997
curl http://0:5000/api/students/53af4926-52ee-41d0-9acc-ae7230209997/courses

# Teacher
curl http://0:5000/api/teachers/53af4926-52ee-41d0-9acc-ae7230400086
curl http://0:5000/api/teachers/53af4926-52ee-41d0-9acc-ae7230400086/courses
