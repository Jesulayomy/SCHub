![SCHub](./landing_page/images/SCHub-removebg-preview.png)

![GitHub contributors](https://img.shields.io/github/contributors/jesulayomy/SCHub?style=for-the-badge&labelColor=%2316161a&color=%237F5AF0) ![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/jesulayomy/SCHub?style=for-the-badge&labelColor=%2316161a&color=%237F5AF0&link=https%3A%2F%2Fgithub.com%jesulayomy%2FSCHub%2Fcommits%2Fmain) ![GitHub language count](https://img.shields.io/github/languages/count/jesulayomy/SCHub?style=for-the-badge&labelColor=%2316161a&color=%237F5AF0) ![GitHub Discussions](https://img.shields.io/github/discussions/jesulayomy/SCHub?style=for-the-badge&labelColor=%2316161a&color=%237F5AF0)![GitHub Issues](https://img.shields.io/github/issues/jesulayomy/SCHub?style=for-the-badge&labelColor=%2316161a&color=%237F5AF0)  ![GitHub repo size](https://img.shields.io/github/repo-size/jesulayomy/SCHub?style=for-the-badge&labelColor=%2316161a&color=%237F5AF0) ![Static Badge](https://img.shields.io/badge/Pre--commit-enabled-red?style=for-the-badge&labelColor=16161a&color=2CB67D)
---
![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstatus&query=status&style=for-the-badge&label=API%20status&labelColor=%2316161a&color=%232CB67D&link=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstatus) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats&query=courses&style=for-the-badge&label=Courses&labelColor=%2316161a&color=%237F5AF0&link=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats&query=students&style=for-the-badge&label=Students&labelColor=%2316161a&color=%237F5AF0&link=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats&query=teachers&style=for-the-badge&label=Teachers&labelColor=%2316161a&color=%237F5AF0&link=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats&query=departments&style=for-the-badge&label=Departments&labelColor=%2316161a&color=%237F5AF0&link=https%3A%2F%2Fschub-api.jesulayomi.tech%2Fapi%2Fstats)

---

## Introduction

SCHub is a webservice that transforms the manner in which institutions, like universities and colleges, handle data storage for students, teachers, departments and courses in a secure and user-friendly setting. It incorporates technologies like MySQL, Python, ReactJS, Nginx and Haproxy to create a robust tech infrastructure for data access and management.
Home: [SCHub](https://schub.jesulayomi.tech/explore)
Article: [Blog post](https://www.linkedin.com/pulse/schub-project-jesulayomi-aina)
Owners: [Aina Jesulayomi](https://www.linkedin.com/in/jesulayomi/) / [Micoliser](https://www.linkedin.com/in/samuel-iwelumo-8a43a6219/)

For accessing the web application for testing purposes, please see [Public Access](#public-access)

---
To contribute to this repo, please see [Contributing](#contributing), [Code of Conduct](CODE_OF_CONDUCT.md), Issues and the Discussions page.

---

## Installation

Clone the repository:

```bash
~ $ git clone https://github.com/Jesulayomy/SCHub.git
~ $ cd SCHub
/SCHub $ python3 -m venv .venv # Create virtual env
/SCHub $ source .venv/bin/activate # Activate virtual env
(.venv) /SCHub $ # Keep the virtual env active
```

Install Python dependencies with [pip](https://pip.pypa.io/en/stable/), set the environment variables, and mysql database user.

```bash
/SCHub $ pip install -r configurations/requirements.txt
/SCHub $ pre-commit install
/SCHub $ cp configurations/environment .env
/SCHub $ vi .env # Use as a guide
...
/SCHub $ mysql -u root -p # Setup mysql user
...
```

Install react dependencies with [npm](https://www.npmjs.com/).

```bash
/SCHub $ cd schub
/schub $ npm -i
```

Run flask app and populate database with data

```bash
/SCHub $ cat data/setup_dev_db.sql | mysql -u root -p
/SCHub $ python3 -m api.app
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.0.2.15:5000
Press CTRL+C to quit
```

On another terminal . . .

```bash
/SCHub $ cd data/
/small $ python3 -m generate_dump.py
/SCHub $ cd ../
/SCHub $ cat data/dump.sql | mysql -u root -p
/SCHub $ curl http://localhost:5000/api/status
{"status": "OK"}
/SCHub $ curl http://localhost:5000/api/stats
{"admins":53,"courses":127,"departments":24,"students":1357,"teachers":32}
```

### Installation – Django

```bash
/SCHub $ cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
# Pending
```


## Usage

### API

GET

```bash
/SCHub $ curl localhost:5000/api/teachers/53af4926-52ee-41d0-9acc-ae7230400015
{"created_at":"2017-03-25T02:17:06","department":"Agricultural Engineering","department_id":"53af4926-52ee-41d0-9acc-ae7230300003","email":"DJUMAR@schub.com","first_name":"DJUMA","id":"53af4926-52ee-41d0-9acc-ae7230400015","last_name":"RINALDO","recovery_question":"What is the name of your childhood best friend?"}
```

DELETE

```bash
/SCHub $ curl -X DELETE http://app.schub.me/api/students/53af4926-52ee-41d0-9acc-ae7230200030 -H  accept: application/json
{}
```

PUT

```bash
/SCHub $ curl -X PUT "http://app.schub.me/api/students/53af4926-52ee-41d0-9acc-ae7230200029" -H  "Content-Type: application/json" -d '{"start_level": 200}'
{"age":28,"created_at":"2017-03-25T02:17:06","current_level":400,"department_id":"53af4926-52ee-41d0-9acc-ae7230300003","email":"JESSIE-JAMIEN@schub.com","first_name":"JESSIE-JAMIE","id":"53af4926-52ee-41d0-9acc-ae7230200029","last_name":"NHIM","matric_no":"202110029JN","recovery_question":"What is your favorite football team?","start_level":200}
```

---

### PUBLIC ACCESS

[API Documentation](https://schub-api.jesulayomi.tech/apidocs/)

You can use the following login details to access the site:
```json
{
  "admin": {
    "email": "tester@schub.com",
    "password": "testerpwd"
  },
  "teacher": {
    "email": "TUANN@schub.com",
    "password": "TUANNPWD"
  },
  "student": {
    "email": "GREAMEM@schub.com",
    "password": "GREAMEMPWD"
  }
}
```

---

### Web page

![architecture](./schub/src/images/architecture.gif)

#### Admins

![Admin Dashboard](./landing_page/images/admin_dashboard.PNG)
![Manage Students](./schub/src/images/student.PNG)
![Update](./schub/src/images/update.PNG)

#### Students

![Student Dashboard](./schub/src/images/student_dash.PNG)

#### Teachers

![Teacher Dashboard](./landing_page/images/teacher_dashboard.PNG)

## Contributing

Pull requests are welcome, but please contact us first. For major changes, please open an issue first to discuss what you would like to change.
Ensure to read the [contribution](CONTRIBUTING.md) and [conduct](CODE_OF_CONDUCT.md) pages.
Please make sure to update tests as appropriate and document changes properly.

### Contributors

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| <img src="https://avatars.githubusercontent.com/u/113533393?s=96&v=4" alt="Jesulayomy" width="80px"> | <img src="https://avatars.githubusercontent.com/u/108087255?v=4" alt="Micoliser" width="80px"> | <img src="https://avatars.githubusercontent.com/u/103280525?v=4" alt="Rani" width="80px"> | <img src="https://avatars.githubusercontent.com/u/124374867?v=4" alt="Shobit" width="80px"> | <img src="https://avatars.githubusercontent.com/u/74444943?v=4" alt="Sreedeep" width="80px"> |
| [Jesulayomy](https://github.com/Jesulayomy) | [Micoliser](https://github.com/micoliser) | [Rani](https://github.com/Rani1303) | [Shobhit](https://github.com/shobhit15082003) | [Sreedeep](https://github.com/Sreedeep-rougeloop) |

## Licensing

MIT License
