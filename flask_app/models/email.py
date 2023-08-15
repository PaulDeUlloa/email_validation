from flask_app.config.mysqlconnection import connect_to_mysql
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class Email:
    DATABASE = "email_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # TO SAVE A SINGLE EMAIL OBJECT IN THE DATABASE
    @classmethod
    def save(cls, data):
        query = "INSERT into email (email) VALUES (%(email)s);"
        return connect_to_mysql(cls.DATABASE).query_db(query, data)

    # GETS ALL the emails from the DATABASE
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM email;"
        results = connect_to_mysql(cls.DATABASE).query_db(query)
        email = []
        for row in results:
            email.append(cls(row))
        return email

    # Class method to delete an email from the datatbase
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM email WHERE id = %(id)s;"
        return connect_to_mysql(cls.DATABASE).query_db(query, data)

    # REGEXCheck and email validation
    @staticmethod
    def is_valid(email):
        is_valid = True
        query = "SELECT * FROM email WHERE email = %(email)s;"
        results = connect_to_mysql(Email.DATABASE).query_db(query, email)
        if len(results) >= 1:
            flash("Email is already taken.")
            is_valid = False
        if not EMAIL_REGEX.match(email["email"]):
            flash("Invalid email address!")
            is_valid = False
        return is_valid
