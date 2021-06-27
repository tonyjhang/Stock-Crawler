import os

PATH = os.path.abspath(os.getcwd())

# for crwaler saving path
IMG_FOLDER = os.path.join(PATH, 'tmp', 'img')
CSV_FOLDER = os.path.join(PATH, 'tmp', 'csv')

# DB info, need to configure, it just a example below
DB_INTERFACE = 'postgresql'
DB_USER_NAME = 'postgres'
DB_PASSWORD = 'test1234'
DB_ADDRESS = 'localhost:5432'
DB_NAME = 'test'