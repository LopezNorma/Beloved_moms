from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




db = 'beloved_moms'

class Mom:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    


    @classmethod
    def get_mom_by_email(cls, data):
        query = "SELECT * FROM moms WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        if len(results)< 1:
            return False
        print('#########################')
        return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM moms"
        results = connectToMySQL(db).query_db(query)
        moms = []
        for row in results:
            moms.append(cls(row))
            return moms
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO moms (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return results
        

    @staticmethod
    def validate_mom(mom):
        is_valid = True
        query = "SELECT * FROM moms WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,mom)
        print(mom['email'],'+++++++++++++++++++++++++++++++')
        if len(results) >= 1:
            flash("Email already taken!!")
            is_valid = False
        if len(mom['first_name']) < 2:
            flash("First name must be at least 2 characters!!")
            is_valid = False
        if len(mom['last_name']) < 3:
            flash('Last name must be at least 3 characters!!')
            is_valid = False
        if not EMAIL_REGEX.match(mom['email']):
            flash('invalid email or password!!!')
            is_valid = False
        if len(mom['password']) < 8:
            flash('password must be at least 8 characters')
            is_valid = False
        if mom['password'] != mom['confirm_password']:
            flash('invalid email or password!!!')
            is_valid = False
            print('################################')
        return is_valid
        
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM moms WHERE id= %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        print('$$$$$$$$$$$$$$$$$$$$$$')
        return cls(results[0])
