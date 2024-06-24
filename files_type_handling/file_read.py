# pandas
import pandas as pd

#database
from  database.database import  *
from  database.db_functions import get_column_names,uploaded_file_data_to_db
#function needs
from .file_write import store_file_on_local
# model
from models.db_model import Reports

def check_file_type(file):
    file_extension = file.filename.rsplit('.', 1)[-1]
    return file_extension



"""
NOTE : READ CSV
1) Getting file and table name as parameter.
2) Processing with Data and return as dictionary.
"""
def read_csv_file(file: str,table_name : str):
    
    # DB CONNECTION
    db: Session = next(get_db())
    
    # DB FUNCTIONS : column names
    get_column_name = get_column_names(table_name,db)
    labels = get_column_name.get('data')[1].get('label_name')
    columns =  get_column_name.get('data')[0].get('column_name')
    
    print('LABEL = ',labels)
    
    try:
    
        # EXCEL OPERATION
        excel = pd.read_csv(file,usecols=labels)
        print('excel = ',excel)
        excel.columns=columns # label to column name
        rows_as_dicts : dict = excel.to_dict(orient='records')
    except:
        pass
    
    return rows_as_dicts
  
        
       



def read_excel_file(file:str, table_name:str):
    
    # DB CONNECTION
    db: Session = next(get_db())
    
    # DB FUNCTIONS : column names
    get_column_name = get_column_names(table_name,db)
    labels = get_column_name.get('data')[1].get('label_name')
    columns =  get_column_name.get('data')[0].get('column_name')
    
    # EXCEL OPERATION
    excel = pd.read_excel(file,usecols=labels)
    excel.columns=columns # label to column name
    rows_as_dicts = excel.to_dict(orient='records')
    
    return rows_as_dicts

    
    
"""
NOTE : UPLOADING FILE
1) Getting file type and tablename as parameter.
2) Checking file type for their function call.
3) Uploading file datas to DB
4) After that Storing file to local for error occured in any columns.
"""

def upload_file(file_type : str, file ,table_name):


    if file_type == 'csv':
        response =  read_csv_file(file,table_name) #reading
        upload_status = uploaded_file_data_to_db(response,table_name) # writing
        store_file =  store_file_on_local(upload_status.get('rows'),table_name) #storing
        # DB CONNECTION
        db: Session = next(get_db())
        
        # REPORTS MODEL
        resport_add = Reports(
                              uploaded_records=upload_status.get('uploaded_record'),
                              un_uploaded_records = int(upload_status.get('un_uploaded_record')),
                              total_no_of_records = upload_status.get('uploaded_record') + upload_status.get('un_uploaded_record'),
                              upload_is_success= True,
                              elapse_time= str(upload_status.get('elapsed_time')),
                              filename = store_file,
                              tablename = table_name
                              
                              
                              )
        db.add(resport_add)
        db.commit()
        print('all is success')

    if file_type == 'xlsx':
      
        response =  read_excel_file(file,table_name) #reading
        upload_status = uploaded_file_data_to_db(response) # writing
        store_file =  store_file_on_local(upload_status.get('rows'),table_name) #storing
        
        # DB CONNECTION
        db: Session = next(get_db())
        
        # REPORTS MODEL
        resport_add = Reports(
                              uploaded_records=upload_status.get('uploaded_record'),
                              un_uploaded_records = int(upload_status.get('un_uploaded_record')),
                              total_no_of_records = upload_status.get('uploaded_record') + upload_status.get('un_uploaded_record'),
                              upload_is_success= True,
                              elapse_time= str(upload_status.get('elapsed_time')),
                              filename = store_file,
                              tablename = table_name
                              
                              
                              )
        db.add(resport_add)
        db.commit()
        print('all is success')
        
        
        
        
        
        
        
        
        
       
    return {
        'status' : 'failed',
        'msg' : 'Invalid file type'
    }





    
    
    
    
 




