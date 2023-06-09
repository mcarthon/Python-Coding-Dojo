# Import the fucntion that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL

# Develop a Class for the data 
class User:
    # pass the data into the class at initialization
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name  = data["last_name"]
        self.email      = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    def __iter__(self):
        for each in self.__dict__.values():
            yield each
        
    # Use >class< methods to query the database
    @classmethod
    def get_all(cls):
        query = """
                SELECT *
                FROM users;
                """
        # Call the connectToMySQL function
        # using the schema/databae name, not
        # the table name
        query_results = connectToMySQL("users_schema").query_db(query)
        
        # create an empty list to append user class instances to
        users = []
        
        # Iterate of the list of dictionaries that are queried from
        # the database
        # Transform the dictionaries into user class instances
        # Then append the user class instances to the users list
        for user in query_results:
            users.append(cls(user))
        
        return users
    
    @classmethod        
    def get_one(cls, id):
        query = """
                SELECT *
                FROM users
                WHERE id = %(id)s;
                """
        query_result = connectToMySQL("users_schema").query_db(query, {"id": id})
        print(query_result)
        user = cls(query_result[0])
        return user
    
    @classmethod    
    def create(cls, data):
        sql_query = """
                    INSERT INTO users
                    (first_name, last_name, email, created_at, updated_at)
                    VALUES
                    (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());
                    """
                               
        return connectToMySQL("users_schema").query_db(sql_query, data) 
    
    @classmethod    
    def update(cls, data):
        sql_query = """
                    UPDATE users
                    SET 
                        first_name = %(first_name)s,
                        last_name  = %(last_name)s,
                        email      = %(email)s,
                        updated_at = NOW()
                    WHERE
                        id = %(id)s;
                    """
        
        return connectToMySQL("users_schema").query_db(sql_query, data)
        
    @classmethod
    def delete(cls, id):
        sql_query = """
                    DELETE FROM users
                    WHERE id = %(id)s;
                    """
        data = {"id": id}
        return connectToMySQL("users_schema").query_db(sql_query, data)
        
    