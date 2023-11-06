import PyPDF2
import uuid


def insert_file(db, user_id, file_id ,file_name, file_url):
    query = f""" 
        SELECT tc.category_id
        FROM tbl_category tc
        WHERE tc.user_id = '{user_id}' AND tc.default_folder_yn = 'Y'
    """
    
    result = db.execute_one(query)
    category_id = result["category_id"]
    
    query = f"""
        INSERT INTO tbl_file (category_id, file_id, file_name, file_url, register_date) VALUES ('{category_id}', '{file_id}', '{file_name}', '{file_url}',CURRENT_TIMESTAMP())
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