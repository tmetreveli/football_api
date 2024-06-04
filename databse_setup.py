import psycopg2

# Connection details
dbname = "football_db"
user = "postgres"
password = "123456"
host = "localhost"  # Change to server IP if remote
port = 5432  # Default PostgreSQL port

try:
    # Connect to the database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Create a cursor object
    c = conn.cursor()


except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
