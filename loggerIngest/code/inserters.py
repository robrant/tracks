from utilities import pg_utilities

def postgresInserter(data):
    ''' Inserts the content into Postgres'''
    
    '''
    Connect to postgres using function above
    Loop data, insert data
    
    ST_AsText(ST_GeomFromGeoJSON(geoJsonStringInHere)) 
    
    Get postgres example
    Get logging example
    
    '''
    
    # Get a database handle to be able to create a new database
    #db, cursor = pg_utilities.pg_connect(db_override=settings.BASE_DATABASE)
    
    # Check if the db exists
    #if cursor.connection.closed == 0:
    #    logging.critical("Failed to connect to initial database: %s" %(settings.BASE_DATABASE), exc_info=True)
    #    return None

    
    db, cursor = pg_utilities.pg_connect()
    
    print dir(cursor)

postgresInserter('hello')
