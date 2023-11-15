import PyPDF2
import uuid
import docx
import requests
from io import BytesIO


def insert_file(db, user_id, file_id ,file_name, file_url, file_size):
    query = f""" 
        SELECT tc.category_id
        FROM tbl_category tc
        WHERE tc.user_id = '{user_id}' AND tc.default_folder_yn = 'Y'
    """
    
    result = db.execute_one(query)
    category_id = result["category_id"]
    
    query = f"""
        INSERT INTO tbl_file (category_id, file_id, file_name, file_url, file_size, register_date) VALUES ('{category_id}', '{file_id}', '{file_name}', '{file_url}', '{file_size}',CURRENT_TIMESTAMP())
    """
    db.execute(query)
    db.commit()
    
    
def get_files(db, user_id):
    query = f"""
        SELECT *
        FROM    tbl_file tf
                LEFT JOIN tbl_category tc ON tf.category_id = tc.category_id
        WHERE tc.user_id = '{user_id}'
    """
    result = db.execute_all(query)
    return result

def request_file_url(url):
    response = requests.get(url)
    return response.content
    
def get_default_category_id(db, user_id):
    query = f""" 
        SELECT tc.category_id
        FROM tbl_category tc
        WHERE tc.user_id = '{user_id}' AND tc.default_folder_yn = 'Y'
    """
    
    result = db.execute_one(query)
    return result["category_id"]

def insert_category(db, category_id, user_id, category_name):
    query = f"""
        INSERT INTO tbl_category
        (category_id, user_id, category_name, register_date, topic_list, default_folder_yn)
        VALUES('{category_id}', '{user_id}', '{category_name}', CURRENT_TIMESTAMP(), NULL, 'N');
    """
    db.execute(query)
    db.commit()


def update_file(db, file_id, category_id):
    query = f"""
        UPDATE tbl_file
        SET category_id = '{category_id}'
        WHERE file_id = '{file_id}'
    """
    db. execute(query)
    db.commit()
    
    
def delete_all_file(db):
    query = f"""
    DELETE
    FROM tbl_file
    """
    db. execute(query)
    db.commit()