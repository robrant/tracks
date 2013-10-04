# SETTINGS FOR INGESTING INTO DB

ELAPSED_TIME_FIELD = 'ElapsedTime'
ABS_TIMESTAMP_FIELD = 'timeStamp'

LAT_FIELD = 'latitude'
LON_FIELD = 'longitude'
GEO_FIELD = 'geojson'

# POSTGRES SETTINGS
BASE_DATABASE = 'postgres'
PREFIX = 'test_'
PG_HOST = 'localhost'
PG_PORT = 5432
PG_DB_NAME = PREFIX + 'tracks'
PG_SCHEMA = 'public'
PG_USER = 'robrant'
PG_PSWD = None #'postgres'

PG_EXTENSIONS = ['postgis', 'pgrouting']

PG_DATA_TABLE = PREFIX + 'x_box_data'