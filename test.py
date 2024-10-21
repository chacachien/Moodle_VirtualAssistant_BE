import asyncpg
from sqlalchemy import create_engine, text

from app.core.config import get_url, get_url_notsync

DATABASE_URL = get_url_notsync() # somwthing like this f'postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}'
import asyncio



# Create a connection to the database
engine =  create_engine(DATABASE_URL)
with engine.connect() as connection:
    # Execute the SQL query to fetch all users
    query = text("""SELECT
                                a.id AS assignment_id,
                                a.name AS assignment_name,
                                a.duedate AS assignment_duedate,
                                s.status AS submission_status
                            FROM
                                mdl_user u
                                JOIN mdl_user_enrolments ue ON u.id = ue.userid
                                JOIN mdl_enrol e ON ue.enrolid = e.id
                                JOIN mdl_course c ON e.courseid = c.id
                                JOIN mdl_assign a ON c.id = a.course
                                LEFT JOIN mdl_assign_submission s ON a.id = s.assignment AND u.id = s.userid
                            WHERE
                                 u.id = 3
                            ORDER BY
                            a.duedate;""")
    result = connection.execute(query)
    print(result.fetchall())

