# Coffee Shop Full Stack

[rubric](https://review.udacity.com/#!/rubrics/2593/view)

[Github](https://github.com/udacity/FSND/tree/master/projects/03_coffee_shop_full_stack/starter_code)


## Tasks

Follow these steps in order to start the application:

1. Prepre the backend
    
    a. [Installe python](https://www.python.org/downloads) & [PostgreSQL](https://www.postgresql.org/download)
    
    b. go to backend folder and run `pip install -r requirements.txt` to install the required packages
    
    c. run these commands to prepare the database
    ```
    dropdb databas
    createdb database
    ```
    
    d. Update `USER_NAME` & `PASSWORD` in `.env` in backend/src/database for the database `username` and `password` respectievly


2. Prepare the frontend
    
    a. [Installe Node.js and NPM](https://nodejs.com/en/download)
    
    b. go to frontend folder and run `npm install` to setup the required packages

    c. update `auth0` data in `frontend/src/enviroments/enviroment.ts` file


3. Run the app
    
    a. go to backend/src and run `flask run`
    
    b. In the frontend folder run `ionic serve`

    c. The application will be accessable from http://localhost:8100


## Udacity NanoDegree notes

- manager login
```
username: tarikgad@gamil.com

password: Qwerty@123456
```

- bariest login
```
username: tarikgad@yahoo.com

password: Qwert@123456
```

- tokens in postman are valid for 24 hours only as a restriction from auth0 since 2018