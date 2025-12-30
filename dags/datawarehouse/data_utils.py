from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table = "yt_api"

def get_conn_cursor():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    conn = hook.get_conn() # connection is used to establish connection to postgres instance

    # cursor is an object that allows you to execute SQL commands for the relevant connection
    # Each row will be returned as a dictionary, not a tuple
    cur = conn.cursor(cursor_factory=RealDictCursor)

    return conn, cur

# close the connection and cursor
def close_conn_cursor(conn, cur):
    cur.close()
    conn.close()

# Uses the cursor and connection to execute an SQL statement to create a schema
def create_schema(schema):
    conn, cur = get_conn_cursor()

    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema}"

    cur.execute(schema_sql)

    conn.commit()

    close_conn_cursor(conn, cur)

# Uses the connection and cursor to execute an SQL statement to create a table. 
# Table will be slightly different if it is in "staging" schema
def create_table(schema):
    conn, cur = get_conn_cursor()

    if schema == 'staging':
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                    "Video_Title" TEXT NOT NULL,
                    "Upload_Date" TIMESTAMP NOT NULL,
                    "Duration" VARCHAR(20) NOT NULL,
                    "Video_Views" INT,
                    "Likes_Count" INT,
                    "Comments_Count" INT   
                );
            """
    else:
        table_sql = f"""
                  CREATE TABLE IF NOT EXISTS {schema}.{table} (
                      "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                      "Video_Title" TEXT NOT NULL,
                      "Upload_Date" TIMESTAMP NOT NULL,
                      "Duration" TIME NOT NULL,
                      "Video_Type" VARCHAR(10) NOT NULL,
                      "Video_Views" INT,
                      "Likes_Count" INT,
                      "Comments_Count" INT    
                  ); 
              """

    cur.execute(table_sql)

    conn.commit()

    close_conn_cursor(conn, cur)

# Returns all video ids in a list
def get_video_ids(cur, schema):

    cur.execute(f"""SELECT "Video_ID" FROM {schema}.{table};""")
    ids = cur.fetchall() # Cursor grabs all remaining rows from the last executed query

    video_ids = [row["Video_ID"] for row in ids] # Store all video ids in list

    return video_ids