from fastapi import FastAPI,UploadFile,File,Depends,Response
from sqlalchemy.orm import Session
# DATABASE FUNCTIONS
from database import db_functions
from database.database import get_db
from database.database import Base,engine

# filetype handling
from files_type_handling import file_read
from files_type_handling.file_write import *
# os
from io import BytesIO
# schema
from schemas.db_schemas import CollectionDetailCreate
#model
from models.db_model import CollectionDetail,Reports


from fastapi.responses import FileResponse
import os
import threading

# CREATING DATABASE
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/download/templates/{table_name}/{file_type}")
async def Gettingt_file(table_name : str, file_type : str,db : Session =Depends(get_db)):
    # Returning file with columns label name
    try:
        
        data = db_functions.get_column_names(table_name,db)
        return reading_file(file_type,data.get('data')[1].get('label_name'),table_name) # RETURN FILE
        
    except Exception as e:
        
        return {
            'status' : 'failed',
            'message' : 'Invalid table name or file type',
            'error' : f"{e}"
        }
        
    
 



@app.post("/upload/templates/{table_name}")
async def Upload_file(table_name : str,file: UploadFile = File(...)):
    # Uploading Templates data 
    try:
    
        contents = await file.read()

        file_data = BytesIO(contents) # convert to bytes object
        file_type = file_read.check_file_type(file) 
        
        thread = threading.Thread(target=file_read.upload_file,args=(file_type,file_data,table_name))
        thread.start()
    
        return {
                'status' : 'success',
                'msg' : 'File uploading started'
            }
    except Exception as e:
        return {
            'status' : 'error',
            'message' : 'Unable to Upload',
            'error' : f"{e}"
        }
    
    
@app.get("/status/templates/{file_name}")
def status_of_upload(file_name : str,db : Session =Depends(get_db)):
    # Sending status of last uploaded file
    
    try:
        
        file_path = file_path = db.query(Reports.filename).order_by(Reports.created_at.desc()).first()
        file_path = file_path[0]+'.xlsx'
        return FileResponse(path=f"status/{file_path}", filename=file_path, media_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return {
            'status' : 'error',
            'message': 'Invalid File name'
        }
    
@app.post("/add_table_column")
async def add_table_column(req: CollectionDetailCreate, db: Session= Depends(get_db)):
    try:
        collection_details = CollectionDetail(**req.dict())
        db.add(collection_details)
        return {
        'status': 'success',
        'msg': 'Row inserted successfully',
        'data' : collection_details
    }
    except Exception as e:
        db.rollback()
        
        return {
            'status': 'failed',
            'msg': f'{e}'
        }
    finally:
        db.commit()

    


@app.get("/records")
def Records_all_details_show(db : Session =Depends(get_db)):
    
    data = db.query(Reports).all()

    return {
        "status" : "success",
        "data" : data
    }


@app.post("/records/{id}")
def Get_record_document_by_id(id :int,db : Session =Depends(get_db)):
    
    try:
    
        file_path = file_path = db.query(Reports.filename).filter(Reports.id==id).first()
        file_path = file_path[0]+'.xlsx'
        return FileResponse(path=f"status/{file_path}", filename=file_path, media_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return {
            'status' : 'failed',
            'message' : 'Invalid id'
        }
    


