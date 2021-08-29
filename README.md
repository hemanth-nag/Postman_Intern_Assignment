# Postman_Intern_Assignment

# Steps to run the program locally:
* Clone the repo.
* Move into the project folder.
* In the terminal, type: 'python app.py' to run the flask app for api data extraction and viewing database.
* Copy, paste the url 'http://localhost:5000/' onto your favorite internet browser.
# Docker Run
* Put this in the terminal: ''
* Now, type: docker run -p 5000:5000 hemanthnag/public_api_scrap
* Copy, paste the url 'http://localhost:5000/' onto your favorite internet browser.
### Home Page
![image](https://user-images.githubusercontent.com/66530316/131257129-acfecb61-6f95-4d3e-85b9-08414f08d26d.png)
* Click on 'View fetched data stored in database' to view the stored database.  
* Click on 'Start 'Public APIs' list scraping' to re-start data fetch (Please view terminal for logs)

# Details of tables:
* I have made two tables:
                         categories(ctgry_id, category)
                         API_list(id2 ,api_name , category , description, auth, https, cors, link)
* Here, API_list.category references categories.ctgry_id as foreign key.
* I have used SQLite3 DBMS beacuse it is light and sufficient for the task. Also, the database and tables get auto-created during execution. 
* Creation of tables externally is not required, but queries are:

    query1 = "CREATE TABLE IF NOT EXISTS categories (ctgry_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, category TEXT)"
    
    query2 = "CREATE TABLE IF NOT EXISTS API_list (id2 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,api_name TEXT, category INTEGER, description TEXT, auth TEXT, https TEXT, cors TEXT, link TEXT, FOREIGN KEY (category) REFERENCES catagories(ctgry_id))"
    
# Points to achieve:

## 1. Your code should follow concept of OOPS

Yes, my code does follow concepts of OOPs. It uses classes and methods for data abtraction, etc.

## 2. Support for handling authentication requirements & token expiration of server

I have created a custom 'request_api' function. This function manages all tasks like getting a new authentication token when it expires, waiting for RATE-LIMIT-RESET, etc.

## 3. Support for pagination to get all data

My code extracts the 'count' data from the response and extracts data from all pages necessary.

## 4. Develop work around for rate limited server

I am currently just haulting the program till the RATE-LIMIT-RESET and continuing further requests.
I tried to find any loop holes and even tried out public proxies as a work-around for rate-limit. But, public proxies are too slow and unsecure.

## 5. Crawled all API entries for all categories and stored it in a database

Yes, I have crawled all 45 API categories and fetched a total of '640' entries.

# Improvements
