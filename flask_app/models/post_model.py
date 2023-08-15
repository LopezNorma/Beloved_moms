from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.mom_model import Mom
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




db = 'beloved_moms'

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = None
        


    @classmethod
    def save(cls, data):
        query = " INSERT INTO posts (name, type, description, mom_id) VALUES (%(name)s, %(type)s, %(description)s, %(mom_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results
    
    @staticmethod
    def validate_post(post_form_data): #This is a dictionary
        is_valid = True
        if len(post_form_data['name']) < 3:
            flash('Name must be at least 3 characters long!!')
            is_valid = False
        if len(post_form_data['type']) < 2:
            flash('type must be at least 2 characters long!!')
            is_valid = False
        if len(post_form_data['description']) < 3:
            flash('description must be at least 3 characters long!!')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_post_w_mom(cls):
        query = """SELECT * FROM posts LEFT JOIN moms ON posts.mom_id = moms.id"""
        results = connectToMySQL(db).query_db(query)
        print('results all post', results)
        posts_by_mom = []
        for post in results:
            one_post = cls(post)
            data={
                'id': post ['moms.id'],
        'first_name': post['first_name'],
        'last_name':post['last_name'],
        'email' : post['email'],
        'password'  :post['password'],
        'created_at' : post['created_at'],
        'updated_at': post['updated_at']
            }
            one_post.posted_by = Mom(data)
            posts_by_mom.append(one_post)
        return posts_by_mom
    
    @classmethod 
    def get_one(cls, post_id):
        data = {"id" : post_id}
        # contructor id must be equal to the one in query
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_post(cls, data):
        query = " UPDATE posts SET name = %(name)s, type = %(type)s, description = %(description)s, mom_id = %(mom_id)s WHERE id= %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def delete_post(cls, post_id):
        data = {"id" : post_id}
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
