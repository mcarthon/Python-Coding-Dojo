from flask_app.config.mysqlconnection import connectToMySQL as conn
from flask import flash
import re
from flask_app import schema, bcrypt

EMAIL_REGEX  = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Loser:        
    
    def __init__(self, data):
        self.id         = data["id"]
        self.first_name = data["first_name"]
        self.last_name  = data["last_name"]
        self.email      = data["email"]
        self.password   = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def get_all(cls):
        
        query = """
                SELECT * 
                FROM losers;
                """
                
        query_results = conn(schema).query_db(query)
        
        losers = []
        
        for loser in query_results:
            losers.append(cls(loser))
            
        return losers    
        
    @classmethod
    def get_other_losers(cls, data):
        
        query = """
                SELECT *
                FROM losers
                WHERE id != %(id)s;
                """               
                
        query_results = conn(schema).query_db(query, data)
        
        other_losers = []
        
        for other_loser in query_results:
            other_losers.append(cls(other_loser)) 
            
        return other_losers            
        
    @classmethod
    def get_loser_by_email(cls, data):
        
        query = """
                SELECT *
                FROM losers
                WHERE email = %(email)s;
                """                               
        
        query_result = conn(schema).query_db(query, data) 
        
        if len(query_result) < 1:
            return False
        return cls(query_result[0])
            
        
    @classmethod
    def get_loser_by_id(cls, data):
        
        query = """
                SELECT *
                FROM losers
                WHERE id = %(id)s;
                """                
                
        query_result = conn(schema).query_db(query, data) 
        
        if len(query_result) < 1:
            return False
        return cls(query_result[0])       
        
    
    @staticmethod        
    def validate_registration(data):
        
        if len(data["first_name"]) < 2:
            flash("First Name must be at least 2 characters long")          
            return False
            
        if len(data["last_name"]) < 2:
            flash("Last Name must be at least 2 characters long")          
            return False            
            
        if not EMAIL_REGEX.match(data["email"]):
            flash("The email you entered is not a valid email address")
            return False
            
        if data["email"] != data["confirm_email"]:
            flash("The two emails you entered did not match")
            return False
            
        losers = Loser.get_all()                    
        emails = [loser.email for loser in losers]
        
        if data["email"] in emails:
            flash("This email has already been registered")
            return False
            
        if len(data["password"]) < 8:
            flash("The password must be at least 8 characters long")
            return False
            
        if data["password"] != data["confirm_password"]:
            flash("The two paswords you entered do not match")
            return False

        return True
        
    @classmethod
    def add_loser(cls, data):               
        
        query = """
                INSERT INTO losers
                (first_name, last_name, email, password)
                VALUES
                (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
                
        return conn(schema).query_db(query, data)     
        
    @staticmethod
    def validate_login(data):
        
        if not Loser.get_loser_by_email({"email": data["email"]}):
            flash("This email has not been registered")        
            return False
            
        loser = Loser.get_loser_by_email({"email": data["email"]})        
              
        if not bcrypt.check_password_hash(loser.password, data["password"]):
            flash("The password does not match our records")    
            return False      
            
        return True         
        
    @classmethod
    def get_sender_data(cls, data):
        
        query = """
                SELECT * 
                FROM exchanges
                JOIN losers
                ON losers.id = exchanges.sender_id
                WHERE exchanges.receiver_id = %(id)s;               
                """           
        query_results = conn(schema).query_db(query, data)
        
        senders = []
        
        for sender in query_results:
            senders.append(cls(sender))
        
        return senders                                                                                                                                                    