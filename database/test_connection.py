import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    try:
        # Menghubungkan ke server MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Berhasil terhubung ke server MySQL Versi: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"Connected to database: {record}")

    except Error as e:
        print(f"Gagal terhubung ke MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Koneksi MySQL ditutup.")

if __name__ == '__main__':
    test_mysql_connection()