# Movies_FlaskApp

Priyanka Shanmugasundaram

https://github.com/prishanmu/Movies_FlaskApp

---

## Project Description

This project has several routes that help a user input movies into the database, visualize ratings for a genre of movies, and look at top rated movies in the database. 

## How to run

1. install all requirements with `pip install -r requirements.txt`
2. then you should run with `python 507project_tools.py runserver`
3. follow the Flask app routes as written below to get to each page

## How to use

1. Follow the routes to get to each part of the application
2. Use the forms to input new data 

## Routes in this application
- `/movie/new` -> this is where to input new movies to the database
- `/top_movies` -> this route lists all movies that have an imdb rating of 8 or above. 
- `/ratings/<genre>` -> this route takes an input and shows a boxplot of the ratings in a genre. 

## How to run tests
1. First install requirements.txt
2. Run the SI507project_tests.py

## In this repository:
- templates
  - index.html
  - all_movies.html
  - all_directors.html
  - forms.html
  - rating_distribution.html
- SI507project_tools.py
- SI507project_tests.py

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [X] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [X] Project is submitted as a Github repository
- [X]  Project includes a working Flask application that runs locally on a computer (not every route works, but yes)
- [X] Includes a clear and readable README.md that follows this template
- [X] Includes a sample .sqlite/.db file
- [X] Includes a diagram of your database schema
- [X] Includes EVERY file needed in order to run the project
- [X] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [X] Includes at least 3 different routes
- [X] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [X] Interactions with a database that has at least 2 tables
- [X] At least 1 relationship between 2 tables in database
- [X] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [X] Use of a new module (Seaborn)
- [X] Use of a second new module (WTForms)
- [X] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [X] A many-to-many relationship in your database structure
- [X] At least one form in your Flask application
- [X] Templating in your Flask application
- [ ] Inclusion of JavaScript files in the application
- [ ] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [ ] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [X] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [ ] Caching of data you continually retrieve from the internet in some way

### Submission
- [X] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [X] I included a summary of my project and how I thought it went **in my Canvas submission**!
