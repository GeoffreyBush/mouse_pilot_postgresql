# MousePilot
## Animal Colony Management System

MousePilot is an open-source web application that provides a centralised repository for tracking mice used in experimentation, and aims to create consistent, real-time data transfer between the site where mice are bred and the site where research is planned and carried out. It is designed to be used by small or medium-sized research facilities that have an in-house breeding facility.

This is a fork of a project that was initially developed as a 3rd year undergraduate software engineering project at the University of Aberdeen in collaboration with the Institute of Medical Sciences at Foresterhill Health Campus. It was forked to replace an SQLite database with PostgreSQL and incorporate Alpine.js and HTMX into the front-end.

---

### Installation instructions

#### Run on localhost

1. Clone this repository. In a terminal, navigate to the root directory ```/mouse_pilot_postgresql/``` that contains ```requirements.txt```

2. Then input the following into your terminal:
```pip -r requirements.txt```
```python manage.py runserver```

3. Open a web browser and navigate to 127.0.0.1:8000 to view the website.

4. Login with username "**SuperUser**" and password "**samplepassword**".

#### Access the deployed version
As an alternative to installation, you can access the deployed version at this URL below. This deployed version is for demonstration purposes only and is not used in production. The database associated with this deployed version of MousePilot may periodically be wiped.:

http://mousepilotabdn.pythonanywhere.com/ 

Login with username "**SuperUser**" and password "**samplepassword**". 

Please note, you will not be able to change the source code or run any Django commands if using this deployed version.  

#### Deployment onto another server

You will need to combine this Django project with a web server such as Apache or Nginx. We cannot currently offer any guidance on this, but there will be tutorials to follow available online.

---

### Database Management

If running the source code, you will find the database ```db.sqlite3```  in the ```/mouse_pilot_postgresql/``` root directory. Django gives you options to apply migrations to the database while in this root directory, which is how Django builds database tables and attributes.

#### Migrations

When making modifications to models.py, the migrations will then need to be applied to the database. You may wish to remove existing migrations and start fresh by deleting all files in ```/website/migrations/``` except ```__init.py__```. If you want to fully reset the database, losing all existing data, also delete ```/mouse_pilot_postgresql/db.sqlite3```. Then run the following commands:
```
# Generate a new migration script
python manage.py makemigrations

# Apply migrations, either creating db.sqlite3 or modifying an existing db.sqlite3
python manage.py migrate
```
Additional documentation on migrations - https://docs.djangoproject.com/en/5.0/topics/migrations/

#### Populating the database
With an empty database and while in the root directory, run:
```python manage.py createfakedata```
This command is customisable by altering ```/website/management/commands/createfakedata.py```

*Note that mothers and fathers are not automatically created. For family tree functionality these will need to be added manually*

--- 

### Testing

There are a comprehensive set of unit and component tests that cover models, views, and forms. This is supplemented with a handful of integration tests that target key functionality, such as login and navigation to certain pages.

These tests will run whenever code is pushed to GitHub. This GitHub workflow can be found in ```./github/workflows/django.yml```

While in the root directory you can use the following commands to run tests manually:

```
# Run all tests
python manage.py test
```

And if you want to generate a coverage report of what code is executed while running all tests, use the Python tool Coverage.
```
coverage run manage.py test
coverage html
```
 The Coverage report will be generated in ```/mouse_pilot_postgresql/htmlcov/```. To alter which files are tracked with Coverage, edit ```/mouse_pilot_postgresql/setup.cfg```:

---

### Changelog

- 0.5
  - Can create mice instances by transferring from breeding cage to stock cage
  - Split "website" Django app into multiple Django apps
  - Converted the application to Bootstrap CSS
- 0.4
  - Breeding cage view
  - Can add comments to mice
  - Family tree display
  - Expanded request task system
  - Python filtering of mice replaced JavaScript
  - Changes to mice can be seen in Edit History
- 0.3
  - Login system
  - Filtering of mice using JavaScript
  - createfakedata script
  - Breeding wing interfaces
  - Researcher can request simple task
- 0.2
  - Creation of database schema
  - Automated pipeline on GitHub
  - Add mouse function
  - Edit mouse function
  - Option to highlight specific mice
- 0.1
  - Can view mouse data in a table
---
### Future Expansions

- Different account types
- Group permissions
- Internal messaging system between users
- Mouse schedule calendar
- "Add Project" functionality
- Transfer mice from breeding cage into stock cage
- Export data for paper printing
- GUI design

---
### Dependencies
- Django v4.2.6
- django-extensions v3.2.3
- Faker v23.2.1
- colorama v0.4.4
- django-filter v24.1
- django-simple-history v3.5.0
- selenium v4.17.2
- chromedriver-autoinstaller v0.6.4
- coverage v7.4.4
- factory_boy v3.3.0
---

### Django Learning Resources

If you want to develop this source code, but are not experienced in Django, here are some useful resources:

Django documentation - https://docs.djangoproject.com/en/5.0/

11-part tutorial that covers Django fundamentals - https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website

Pyplane YouTube channel - https://www.youtube.com/@Pyplane

BugBytes YouTube channel - https://www.youtube.com/@bugbytes3923

---
#### Group Members 2023-24:

- Zachary Jacobson (1st term)
- Yusuf Qureshi (2nd term)
- Rhys Speers
- Shu Fan Sun
- Geoffrey Bush
- Jingfeng Chen
- Osman Elyas

---