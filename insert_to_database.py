from mysql.connector import MySQLConnection, Error
from face_detection_dbconfig import read_db_config

# call function to insert face data 
def insert_face_data(face_id, gender, age, emotion, emotion_percent):
    # mysql statement
    query = "INSERT INTO FaceData(face_id, gender, age, emotion, emotion_percent) " \
            "VALUES(%s,%s,%s,%s,%s)"
            # argument to be passed
    args = (face_id, gender, age, emotion, emotion_percent)
 
    try:
        # connect to database
        db_config = read_db_config.read_db_config()
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(query, args)
        # print insert id
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        # commit to insertion
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        # close connection
        cursor.close()
        conn.close()
        print("Face Data Inserted To Database")



'''
def main():
   insert_face_data()
 
if __name__ == '__main__':
    main()
'''