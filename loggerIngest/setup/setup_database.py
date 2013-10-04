''' 
Builds the database, schema, tables and functions.
'''
import os
import logging
import subprocess
from config import ingestSettings as settings
from utilities import pg_utilities
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Setup Logging
logFile = os.path.join(settings.LOG_DIRECTORY, settings.DB_SETUP_LOG_FILE)
logging.basicConfig(filename=logFile, format='%(levelname)s:: \t%(asctime)s %(message)s', level=settings.DB_SETUP_LOG_LEVEL)

#------------------------------------------------------------------------------------------------------------------

def get_postgres_extensions_list(db, host, port, user):
    ''' List all extensions available under this database'''
    ext_names = []
    cmd =['psql', '--database=%s'%db, '--host=%s'%host, '--port=%s'%port, '--username=%s'%user, '-c', '\dx']
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    lines = out.stdout.readlines()[3:]
    for line in lines:
        line = line.strip()
        line_split = line.split()
        if (line_split[0] == '|' and (len(line_split[0]) == 1)): # assume there is no database titled '|'
            return ext_names
        ext_names.append(line_split[0])
    
    return ext_names

#------------------------------------------------------------------------------------------------------------------

def get_postgres_database_list(host, port, user, password):
    ''' List all the databases on this host'''
    
    db_names = []
    cmd = ['psql', '--host=%s'%host, '--port=%s'%port, '--username=%s' %user, '--list']
    
    if password:
        print 'Using password: %' %password
        cmd.append("--password=%s" % password)
    else:
        cmd.append("--no-password")

    out = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    lines = out.stdout.readlines()[3:]
    for line in lines:
        line = line.strip()
        line_split = line.split()
        if (line_split[0] == '|' and (len(line_split[0]) == 1)): # assume there is no database titled '|'
            return db_names
    curr_db_name = line_split[0]
    db_names.append(curr_db_name)
    return db_names

#------------------------------------------------------------------------------------------------------------------

def add_extension(db, host, port, user, password, db, extension):
    ''' Adds an extension, assumed to be installed '''
    
    # Add POSTGIS extension via command line
    add_ext = ['psql', '--host=%s'%host, '--port=%s'%port, '--username=%s'%user, '--database=%s' %db, '-c', "CREATE EXTENSION %s;" %extension]
    if password:
        print 'Using password: %' %password
        add_ext.append("--password=%s" % password)
    else:
        add_ext.append("--no-password")
        
    subprocess.Popen(add_ext)

#------------------------------------------------------------------------------------------------------------------

def drop_db(host, port, user, password, db):
    ''' Drop the database'''
    
    drop_db = ['DROPDB ', '--host=%s'%host, '--port=%s'%port, '--username=%s'%user, '%s'%settings.db]
    if password:
        print 'Using password: %' %password
        drop_db.append("--password=%s" % password)
    else:
        drop_db.append("--no-password")

    subprocess.Popen(drop_db)

#------------------------------------------------------------------------------------------------------------------

def create_db(host, port, user, password, db):
    ''' Create the database'''
    
    drop_db = ['CREATEDB ', '--host=%s'%host, '--port=%s'%port, '--username=%s'%user, '%s'%settings.db]
    if password:
        print 'Using password: %' %password
        drop_db.append("--password=%s" % password)
    else:
        drop_db.append("--no-password")

    subprocess.Popen(drop_db)

#------------------------------------------------------------------------------------------------------------------

def build_db():
    
    
    host = settings.PG_HOST
    port = settings.PG_PORT
    user = settings.PG_USER
    pswd = settings.PG_PSWD
    
    # List the current DBs
    db_list = get_postgres_database_list(host, port, user, pswd)
    
    # Drop the database if its not in the current list
    if settings.PG_DB_NAME in db_list and settings.DROP_DB == True:
            drop_db(host, port, user, pswd, settings.PG_DB_NAME)
    
    # Create the db        
    create_db(host, port, user, pswd, settings.PG_DB_NAME)
    
    # add extensions via command line
    for extension in settings.PG_EXTENSIONS:
        add_extension(extension)

    # Check that the extensions have all been installed
    registered_extensions = get_postgres_extensions_list(settings.PG_DB_NAME, host, port, user)
    for ext in settings.PG_EXTENSIONS:
        if ext.lower() not in registered_extensions:
            logging.error('Failed to add extension (%s) to the database (%s)' %(ext, settings.PG_DB_NAME))
        

    