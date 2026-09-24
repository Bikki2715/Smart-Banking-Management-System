import psycopg2


try:
    connection = psycopg2.connect(
        host="localhost",
        database="smart_banking",
        user="postgres",
        password="481141",
        port="5432"
    )

    print("\n========================================")
    print("   DATABASE CONNECTION SUCCESSFUL")
    print("========================================")

    connection.close()

except psycopg2.Error as error:

    print("\n========================================")
    print("   DATABASE CONNECTION FAILED")
    print("========================================")
    print("Error:", error)