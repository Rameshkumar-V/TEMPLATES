from models.db_model import CollectionDetail,User
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from schemas.db_schemas import UserBase
from .validation import *
import time



"""
NOTE : Get column Names
1) Getting column details with help of their tablename
2) response with column name, type,label,error_msg
"""
def get_column_names(table_name,db: Session = next(get_db())  ):
    try:
        
        # DB QUERY
        column_names = db.query(CollectionDetail.column_name,CollectionDetail.label,CollectionDetail.column_type,CollectionDetail.error_msg).filter(
            CollectionDetail.table_name == table_name
        ).all()
        

        column_names_list = [column_name[0] for column_name in column_names]
        label_names_list = [column_name[1] for column_name in column_names]
        column_type = [column_name[2] for column_name in column_names]
        column_error_msg = [column_name[3] for column_name in column_names]
        

        return {
            'status': 'success',
            'data' : [
                {
                    'column_name':column_names_list
                },
                {
                    'label_name': label_names_list
                },
                {
                    'column_type' : column_type
                    
                },
                {
                    'error_msg' : column_error_msg
                }
                ]  
        }
    except Exception as e:
        raise e
        
        print('error on get_column_name: ',e)
        return {
            'status': 'error'
        }
        



def uploaded_file_data_to_db(datas : list):
    # Start the timer
    start_time = time.time()
    rows = []
    uploaded_record = 0
    unuploaded_record = 0
    
    # DB FUNCTIONS 
    db: Session = next(get_db())   # db session for normal function
    get_column_name = get_column_names('user')
    
    column_types = get_column_name.get('data')[2].get('column_type')
    column_name = get_column_name.get('data')[0].get('column_name')
    label_name = get_column_name.get('data')[1].get('label_name')
    column_error =  get_column_name.get('data')[3].get('error_msg')
    
    # name with type used for validating.
    columns = dict(zip(column_name,column_types))  
      
    for data in datas:
        try:
            
            data_column_name = data.keys()
            data_column_values = data.values()
        
            # NOTE : column name means label name becuase in file they label name was used, so they mention as files column name.
            zibbed = list(zip(data_column_name,data_column_values,column_error,label_name))
            
            # Error variable used to store error
            errors =""
            
            for column_name, column_data,c_error,label in zibbed:
                
                # Validating with type
                
                if columns.get(column_name) == 'String':
                    r=StringValidator.is_valid(string=column_data)
                    if not r:
                        errors= errors+'\n'+f'<{label} : {c_error}>'
                    
                if columns.get(column_name) == 'Integer':
                    r=IntValidator.is_valid(number=column_data)
                    if not r:
                        errors= errors+'\n'+f'<{label} : {c_error}> '
                if columns.get(column_name) == 'Email':
                    r=EmailValidator.is_valid(email=column_data)
                    if not r:
                        errors= errors+'\n'+f'<{label} : {c_error}>'
                    
                    
        
            
            # print('database operation start soon')
            user_to_db = User(**data) #model
            db.add(user_to_db)
            
            if errors=="":
                uploaded_record = uploaded_record +1
            
                rows.append({
                    
                    'row' : data,
                    'error' : errors,
                    'status' : 'uploaded'
                    
                })
                
            else:
                un_uploaded_record = un_uploaded_record +1
                
                rows.append({
                    'row' : data,
                    'error' : errors,
                    'status' : 'un uploaded'
                })
                    
                    
        except Exception as e:
            
            unuploaded_record = unuploaded_record +1
            rows.append({
                
                'row' : data,
                'error' : f'field unavilable : '.join(errors),
                'status' : 'un uploaded'
                
              
            })
        db.rollback()
        
        
   
    end_time = time.time()
    elapsed_time = end_time - start_time

   
    return {
        'rows':rows,
        'uploaded_record':uploaded_record,
        'un_uploaded_record':unuploaded_record,
        'start_time':start_time,
        'end_time':end_time,
        'elapsed_time':elapsed_time
        }
    
            
            
        
