from fastapi import Response
import pandas as pd
from io import BytesIO
import time
from database.db_functions import get_column_names



# EXCEL
def write_as_excel(table_name,data : list):
    
    # buffer used to create virtual memory
    buffer = BytesIO()

    # EXCEL OPERATIONS
    df = pd.DataFrame([data], columns=data)
    df.to_excel(buffer, index=False,header=False)
    
    # Get the byte value of the buffer
    buffer.seek(0)
    file_bytes = buffer.getvalue()
    
    # Return the Excel file as a response
    return Response(content=file_bytes, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={
            "Content-Disposition": f"attachment; filename={table_name}.xlsx"
        })

# CSV
def write_as_csv(table_name: str, data: list):
   
    buffer = BytesIO()
    df = pd.DataFrame(data)
    df.to_csv(buffer, index=False, header=True)

    buffer.seek(0)
    file_bytes = buffer.getvalue()
    
    # Return the CSV file as a response
    return Response(
        content=file_bytes,
        media_type="application/csv",
        headers={
            "Content-Disposition": f"attachment; filename={table_name}.csv"
        }
    )

def reading_file(file_type : str,data : str, table_name : str):
    
    if file_type == 'xlxs':
        return write_as_excel(table_name,data)
    if file_type == 'csv':
        return write_as_csv(table_name,data)
    
    
    return {
        'status' : 'failed',
        'message' : 'Invalid File Type'
    }
        

def store_file_on_local(upload_status,table_name):
    """
    Storing file on local status folder
    """
    
    # DB FUNCTIONS
    get_column_name= get_column_names(table_name=table_name)
    labels = get_column_name.get('data')[1].get('label_name')

    dataframe_data = []
    for row in upload_status:
       
        error : str = row.get('error') # if error occured then error msg stored.
        status : str = row.get('status') # status have uploaded or un uploaded.
        data : dict =  row.get('row') # row have all data for wanted by column.

        data.update({'error':error,'status' : status}) # update the dictionary for adding column error and status.
        
        if status == 'un uploaded':
            # adding data only row contains error
            dataframe_data.append(data)
        
    # EXCEL OPERATIONS    
    excel_file = pd.DataFrame(dataframe_data)
    excel_file.columns=labels+["error","status"]
    filename = str(table_name) + str(time.time())
    excel_file.to_excel(f'status/{filename}.xlsx',index=False) # storing local status folder
    
    return filename
    
