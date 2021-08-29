import sqlite3
import requests
import math
import time

class Database():
    """
    Class that handles database
    """
    
    def __init__(self, db_filename): 
        self.db_file = db_filename
        self.conn = None
        self.cur = None
        
    def get_connection(self):
        """
        Get connection to the database
        """
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()
        print("Database Created!!")
        
    def create_tables(self):
        """
        Create the two tables: Categories and API_list
        """
        query1 = "CREATE TABLE IF NOT EXISTS categories (ctgry_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, category TEXT)"
        query2 = "CREATE TABLE IF NOT EXISTS API_list (id2 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,api_name TEXT, category INTEGER, description TEXT, auth TEXT, https TEXT, cors TEXT, link TEXT, FOREIGN KEY (category) REFERENCES catagories(ctgry_id))" 
        
        self.cur.execute(query1)
        self.cur.execute(query2)
        self.conn.commit()
        print("Tables Created")
        
    def insert_categories(self, categories_list):
        """
        Insert categories into the table
        """
        print("Inserting Categories to database")
        for cat in categories_list:
            query1 = f"INSERT INTO categories(category) VALUES ('{cat}')"
            self.cur.execute(query1)
        
        self.conn.commit()
    
    def insert_rows(self, rows):
        """
        Insert all api data into the table: api_list. References Categories table
        """        
        for row in rows:
            query1 = "INSERT INTO API_list(category, api_name , description, auth, https, cors, link) VALUES ('" + str(row[0]) + "', '" + row[1] + "', '" + row[2] + "', ' " + row[3] + "', '" + str(row[4]) + "', '" + str(row[5]) + "', '" + str(row[6]) + "')"
            self.cur.execute(query1)
        
        self.conn.commit()
        
           
    
    def __del__(self):
        """
        Destructor
        """
        print("Database Closed")
        self.cur.close()
        self.conn.close()
        
        
class API_Extraction():
    """
    Class handling api calls and insertion.
    """
    
    def __init__(self):       
        self.database = Database("api_data.db")
        self.database.get_connection()
        self.database.create_tables()
        
        self.auth_header = None
        self.auth_url = "https://public-apis-api.herokuapp.com/api/v1/auth/token"
        
        self.categories = []
    
    
    def request_api(self, url, header = {}):
        """
        Custom request function to handle authorizarion, rate-limit-waiting and return responses. 
        """
        while(True):
            try:
            
                response = requests.request("GET", url, headers=self.auth_header, data={})
                if(response.status_code == 403):
                    print("fetching new auth key")
                    self.get_api_auth()

                elif(response.status_code == 429):
                    while(float(time.time())<float(response.headers['X-Ratelimit-Reset'])):
                        print("Waiting for Rate-Limit-Reset")
                        time.sleep(2)

                elif(response.status_code == 200):
                    break
            except Exception as e:
                print(e)
        
        return response.json()
    
    
    def get_api_auth(self):
        """
        Get api authorizarion header key
        """
        try:
            response = requests.request("GET", self.auth_url, headers={}, data={}).json()
            val = f"Bearer {response['token']}"
            self.auth_header = {"Authorization": val}
        except:
            pass
    
    def get_categories_from_api(self):
        """
        Get all categories from api and pass to insert_categories function for database insert.
        """
        url = "https://public-apis-api.herokuapp.com/api/v1/apis/categories?page=1"
        
        print("Starting Categories Extraction")
        resp = self.request_api(url = url, header = self.auth_header)
        page_count = math.ceil(resp["count"]/10)
        self.categories.extend(resp["categories"])

        for pg_no in range(2, page_count+1):

            url = f"https://public-apis-api.herokuapp.com/api/v1/apis/categories?page={pg_no}"
            response = self.request_api(url = url, header = self.auth_header)
            self.categories.extend(response["categories"])
        self.database.insert_categories(self.categories)
        
        print("Fetched and inserting all categories done!!!     Count:", len(self.categories))
            
    

    def get_all_apis_list(self):
        """
        Get all categories api data from the server api and pass it to insert_rows function for database insert.
        """
        for id1, ctgry in enumerate(self.categories):
            
            category_dicts = []
            category_rows=[]
            req_data = ["API", "Description", "Auth", "HTTPS", "Cors", "Link"]
            ctgry = ctgry.replace("&","%26")
            url = f"https://public-apis-api.herokuapp.com/api/v1/apis/entry?page=1&category={ctgry}"
            
            response = self.request_api(url = url, header = self.auth_header)
            
            page_count = math.ceil(response["count"]/10)
            category_dicts.extend(response["categories"])
            
            for pg_no in range(2, page_count+1):
                
                url = f"https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={pg_no}&category={ctgry}"
                response = self.request_api(url = url, header = self.auth_header)
                category_dicts.extend(response["categories"])
            
            for res_dict in category_dicts:
                row = [id1+1]
                for key in req_data:
                    row.append(res_dict[key])
                category_rows.append(row)              
            for i in range(len(category_rows)):
                category_rows[i] = [x.replace('\'', '') if type(x)==str else x for x in category_rows[i]]
            self.database.insert_rows(category_rows)
            print(f"Fetching and inserting {ctgry} done!!    Count: {len(category_rows)}")
            
def main():
    
    api = API_Extraction()
    
    api.get_categories_from_api()
    
    api.get_all_apis_list()
    
    print("Extraction of all data successful!!")
    
if __name__ == '__main__':
    main()  
    