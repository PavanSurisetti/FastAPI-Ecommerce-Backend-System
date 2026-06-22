#this file contains all the database connections and engine creation and sessoin creation
#this is used to load the environmental variables
from dotenv import load_dotenv
#this is used to create a base class for all tables and sessionmaker is used to create sessions
from sqlalchemy.orm import declarative_base,sessionmaker
#this is used to create a connection to database
from sqlalchemy import create_engine
import os
#loading varibles from .env
load_dotenv()
DATABASE_URL=os.getenv('DATABASE_URL')
#let's create a engine
engine=create_engine(DATABASE_URL)
#let's create Base class 
Base=declarative_base()
#let's create a session
SessionLocal=sessionmaker(bind=engine)