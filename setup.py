from DB_structure import create
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from settings import DB_INTERFACE, DB_USER_NAME, DB_PASSWORD, DB_ADDRESS, DB_NAME


engine = create_engine(
    f'{DB_INTERFACE}://{DB_USER_NAME}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'
)

if not database_exists(engine.url):
    create_database(engine.url)

#init DB
create(engine)