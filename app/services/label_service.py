
from sqlmodel import select, delete, insert
from fastapi import HTTPException
from starlette import status
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text


DATABASE_URL = get_url_notsync()
print(DATABASE_URL)
class LabelService(object):
    __instance = None
    engine = create_engine(DATABASE_URL)
    def __init__(self):
        pass

    @staticmethod
    def get_all_label():
        try:
            with LabelService.engine.connect() as connection:
                query = text('SELECT * FROM mdl_label')
                result = connection.execute(query)
                rows = result.fetchall()
                # convert result to json and return 
                label_list = []
                for row in rows:
                    print(row)
                    label = {
                        'id': row[0],
                        'course': row[1],
                        'name': row[2],  # Assuming the name field is the first column in the query result
                        'intro': row[3],
                        'timemodified': row[5]                    }
                    label_list.append(label)
                print(label_list)
                # Return the list of JSON objects
                return label_list
        except Exception as e:
            print(e)

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
def main():

    lis_Label = LabelService.get_all_label()
    
    print(lis_Label)

if __name__ == '__main__':
    main()