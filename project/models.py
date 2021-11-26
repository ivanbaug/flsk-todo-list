from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # User has a parent relationship with respect to Tasks and TDList
    # This will act like a List of TDLists objects attached to each User.
    # The "author" refers to the author property in the TDList class.
    ulists = relationship("TDList", back_populates="author")
    tasks = relationship("Task", back_populates="task_author")


# Cafe TABLE Configuration
class TDList(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, unique=True, nullable=False)
    all_done = db.Column(db.Boolean)
    #  TDList is child of user
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("User", back_populates="ulists")

    # TDList has a parent relationship with respect to Tasks
    tasks = relationship("Task", back_populates="parent_list")

    def to_dict(self):

        # Method 1.
        mydict = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            mydict[column.name] = getattr(self, column.name)
        return mydict

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, nullable=False)
    # TODO: Possible future feature
    expires_on = db.Column(db.DateTime)

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    task_author = relationship("User", back_populates="tasks")

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    list_id = db.Column(db.Integer, db.ForeignKey("todolist.id"))
    # Create reference to the User object, the "cafes" refers to the cafes property in the User class.
    parent_list = relationship("TDList", back_populates="tasks")
