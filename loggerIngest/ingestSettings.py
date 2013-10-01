# SETTINGS FOR INGESTING INTO DB

ELAPSED_TIME_FIELD = 'ElapsedTime'
ABS_TIMESTAMP_FIELD = 'timeStamp'

# POSTGRES SETTINGS
PREFIX = 'test_'
PG_HOST = 'localhost'
PG_PORT = 5432
PG_DB_NAME = PREFIX + 'tracks'
PG_SCHEMA = 'public'
PG_USER = 'postgres'
PG_PSWD = 'postgres'

PG_DATA_TABLE = PREFIX + 'x_box_data'