from fastapi import HTTPException
from starlette import status
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, text


DATABASE_URL = get_url_notsync()
print(DATABASE_URL)
class SystemService(object):
    __instance = None
    engine = create_engine(DATABASE_URL)
    def __init__(self):
        pass

    @staticmethod
    def get_all_course():
        try:
            with SystemService.engine.connect() as connection:
                query = text("SELECT id, fullname, summary FROM mdl_course where category != 0") #### or topics 
                result = connection.execute(query)
                rows = result.fetchall()
                # convert result to json and return 
                course_list = []
                for row in rows:
                    label = {
                        'id': row[0],
                        'name': row[1],
                        'summary': row[2]
                        }
                    course_list.append(label)

                # convert result to document
                import json
                json_string = json.dumps(course_list)

                return json_string
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    


def main():
    info = SystemService.get_all_course()
    print(info)

if __name__ == "__main__":
    main()
        