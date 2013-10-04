
# Ensure this project is on the path
import sys
projectPath = '/Users/robrant/eclipseCode/tracks/loggerIngest'
if projectPath not in sys.path:
    sys.path.append(projectPath)

import psycopg2
from config import ingestSettings as settings

#------------------------------------------------------------------------

def pg_connect(db_override=None):
    
    if db_override:
        db = db_override
    else:
        db = settings.PG_DB_NAME
    
    db = psycopg2.connect(database=db,
                          host=settings.PG_HOST,
                          port=settings.PG_PORT,
                          user=settings.PG_USER,
                          password=settings.PG_PSWD)

    cursor = db.cursor()
    
    return db, cursor 

#------------------------------------------------------------------------
