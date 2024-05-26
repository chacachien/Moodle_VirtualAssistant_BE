
from cmd import PROMPT
from langchain import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

PROMPT_CHOOSE_TOOLS_TEMPLATE = """You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:
            {rendered_tools}
            Given the user input, return the name and input of the tool to use. The input of the tool is {input}. Return your response as a JSON blob with 'name' and 'arguments' keys.
            Just use those tool that given, not try to access anything else. If you don't know what is the right tool, just use the "talk" tool.
            INPUT: {input}
            Remember Return your response as a JSON blob with 'name' and 'arguments' 
            EXAMPLE: 
                    + "name": "talk", "arguments": "question": "Chào cậu"
                    + "name": "rag", "arguments": "question": "Giải thích sự tăng trưởng của Việt Nam"
                    + "name": "query", "arguments: "question: "tôi đang tham gia những khóa học nào"
            RESPONSE: 
            """

PROMPT_CHOOSE_TOOLS = PromptTemplate.from_template(PROMPT_CHOOSE_TOOLS_TEMPLATE)

PROMPT_CHOOSE_TOOLS_V1 = ChatPromptTemplate.from_messages(
    [
        ("system", PROMPT_CHOOSE_TOOLS_TEMPLATE),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

PROMPT_NORMAL_TALK = PromptTemplate.from_template("""
            You are my funny virtual assistant.
            Context: {context}
            User: {input}
            Answer:
            """
        )

PROMPT_REMINDER = """You should be a responsible ChatGPT and should not generate harmful or misleading content! 
Please answer the following user query in a responsible way."""


PROMPT_RAG = PromptTemplate.from_template("""
            You are a document teller. These Human will ask you a questions about their document. 
            Use following piece of context to answer the question. 
            If you don't know the answer, just say you don't know. 
            Keep the answer within 2 sentences and concise.

            Context: {context}
            User: {question}
            Answer: 
            """
        )
PROMPT_RAG_IMPROVE = PromptTemplate.from_template("""
            ## Expert persona: You function as an AI assistant within a course system, specializing in providing guidance and assistance to users regarding course content.
            ## User: {question}
            ## Context: {context}
            ## Goal: Offer clear and helpful responses to users' inquiries related to the course content.
            ## Instructions:
                1. Use the provided course content to craft accurate responses.
                2. If uncertain, politely inform the user that you don't have the answer.
                3. When confident, provide concise and insightful assistance, not just itemize.

            ## Constraints:
                + Only use the content of Context to answer user.
                + Ensure responses remain pertinent to the course material.
                + Avoid referencing information not contained within the course context.
                + Prompt users to furnish additional context if required.
                + Maintain professionalism and clarity in all interactions.
                + Respond in a language consistent with that used by the user.
            ## YOU ANSWER: 
    """)

PROMPT_REMIND_TO_COURSE = PromptTemplate.from_template("""
        ## Expert persona: You function as an AI assistant within a course system, your task is to send a message to remind the user to go to the course page.
        ## User: {input}
        ## Course information: {context}
        ## Goal: Offer clear and helpful responses to users' inquiries related to the course content.
        ## Instructions:
            1. Use the information of the course in the system to remind the user to go to the course page that is relevant to the user's question.
            2. If the course information is not relevant to the user's question, just say the system does not have any course that is relevant to the user's question and do nothing further. 
            3. Otherwise, if the user message and course information match, remind the user to visit the course page to get more information. Link to course page: 
                http://localhost/moodle/course/view.php?id=[courseid]
        ## Constraints:
            + Ensure the reminder is polite and encouraging.
            + Provide a friendly and helpful message to the user.
            + Use the user's language and tone in your response.
            + Just remind in 2 sentences.
            + Do not give a reminder if the course information and user's question do not match. Only remind when they match.
            + Do not create responses like this: "Xin chào, bạn có thể tìm hiểu về ML trong khóa học 'Lịch sử và văn hóa của Việt Phục qua các thời kỳ'. Hãy truy cập trang khóa học để biết thêm thông tin nhé!" because ML and "Lịch sử và văn hóa của Việt Phục qua các thời kỳ" do not match. In that case, just sorry user about it. 
        ## YOUR ANSWER:
            // YOUR ANSWER HERE
    """)
# PROMPT_REMIND_TO_COURSE = PromptTemplate.from_template(
#             """
#             ## CONTEXT: 
#                 You are an AI assistant within a learning management system (LMS).
#                 Your primary function is to assist users with course-related inquiries.
#             ## USE SCENARIO:
#                 0. Receive user input: {input}
#                 1. Receive Response from First Chatbot: You receive the initial response ({message}) from the first chatbot.
# `               2. Base on the user input and the first response to make the Course Relevance Check:
#                     Match Found: Remind the user to visit the course page to get more information.
#                     No Match (by First Chatbot): If the first chatbot can not answer, say no course that relevant to the question.

#             ## Additional Considerations:
#                 Language and Tone: Always maintain a friendly, helpful, and polite tone, mirroring the user's communication style as much as possible.
#                 Proactive Assistance: If you can anticipate user needs based on their browsing history or past interactions, offer proactive suggestions for relevant courses.
#                 Just remind in 2 sentences.

#             ## Output:
#                 // Your output here
#             """)
                                                       


# PROMPT_STRUCTURE_TABLE = PromptTemplate.from_template(
#             """You are a data expert. Given the question and and the table information, decide what is the part of data structure that remain and delete the rest.
#             Question: {question}
#             Database Structure: {database_structure}
#             Output: 
#             // Your data structure (schema) here
#             """
#         )

PROMPT_STRUCTURE_TABLE = PromptTemplate.from_template(
            """
            ## Expert persona: You are a data expert. Given the question and the table information, determine the tables will be remain and remove the rest.
            ## User: {question}
            ## Database Structure: {database_structure}
            ## Goal: Identify and retain the pertinent part of the table list.
            ## Instructions:
                1. Analyze the provided question and table list.
                2. Determine the essential part of the table list that use for SQL query.
                3. Remove any irrelevant parts of the data structure.
                4. Return the table list that remains.
            ## Contraint:
                + Must remain the information of that table include: useable, candidate value, purpose
                + Must remain all column of each table.
            ## Output:
                // Your data structure (schema) here

            """)










# PROMPT_SQL_QUERY = PromptTemplate.from_template(
#             """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.
#             And you also a virtual assistant for user {id}.
#             Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
#             You just only use SELECT command to get data. Don't do anything that can effect into table.
#             Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
#             Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".
#             Remember to Use "SELECT FROM_UNIXTIME(MAX(DATE))" when get the data that relevant to date time (like startdate, enddate) because it store with bigint type in mysql.
#             Question: {question}
#             Database Structure: {database_structure}
#             Just return the SQL code. Do not include anything.
#             SQL: // Your SQL query here
#             """
#         )
PROMPT_SQL_QUERY = PromptTemplate.from_template(
            """
            ## Expert persona: You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. 
            ## Question: {question}
            ## User ID: {id}
            ## Database Structure: {database_structure}
            ## Goal: Generate a correct and efficient MySQL query based on the input question.
            ## Instructions:
                1. Construct a SELECT query to retrieve data relevant to the question.
                2. Use the LIMIT clause to return at most 5 results, unless otherwise specified by the user.
                4. Use only the column names present in the provided tables.
                5. Ensure queries do not modify the database; use SELECT commands only.
                6. Utilize the CURRENT_DATE function for queries involving "today."
                7. Use "SELECT FROM_UNIXTIME(MAX(DATE))" for datetime columns stored as bigint in MySQL.
            ## Constraints:
                + Do not query columns that do not exist.
                + Be precise about which column belongs to which table.
                + Ensure the query is syntactically correct.
                + Return the SQL code only.
                + Do not call user by their id.
            ## Example:
                - Question: "Tôi đang tham gia khoa học nào?"
                - Output:   SELECT c.id AS course_id, c.fullname AS course_name, ue.timestart AS enrolment_start, ue.timeend AS enrolment_end
                            FROM mdl_user u
                            JOIN mdl_user_enrolments ue ON u.id = ue.userid
                            JOIN mdl_enrol e ON ue.enrolid = e.id
                            JOIN mdl_course c ON e.courseid = c.id
                            WHERE u.id = :user_id
                            ORDER BY ue.timestart DESC
                            LIMIT 5;
                - Question: "Tôi đang có những bài quiz nào?",
                - Output:   SELECT q.id AS quiz_id, q.name AS quiz_name, c.id AS course_id, c.fullname AS course_name
                            FROM mdl_user u
                            JOIN mdl_user_enrolments ue ON u.id = ue.userid
                            JOIN mdl_enrol e ON ue.enrolid = e.id
                            JOIN mdl_course c ON e.courseid = c.id
                            JOIN mdl_quiz q ON q.course = c.id
                            WHERE u.id = :user_id
                            ORDER BY c.fullname, q.name
                            LIMIT 5;
                - Question: "tôi đang có những assignment nào?", 
                - Output: 'SELECT
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
                                u.id = :user_id
                            ORDER BY
                            a.duedate;'
            ## Output:
                // Your SQL query here
            """
        )

# PROMPT_FIX_BUG = PromptTemplate.from_template(
#             """You are a MySQL expert. Given the SQL code and the error. Help me fix it.
#             Use the following format:
#             User id: {id}
#             Question: {question}
#             Database Structure: {database_structure}
#             SQL code: {SQL_code}
#             Error: {Error}
#             Just return the SQL code. Do not include anything.
#             SQL: // Your SQL query here
#             """
#         )
PROMPT_FIX_BUG = PromptTemplate.from_template(
            """
            ## Expert persona: You are a MySQL expert. Given the SQL code and the error, assist in fixing it.
            ## User id: {id}
            ## Question: {question}
            ## Database Structure: {database_structure}
            ## SQL code: {SQL_code}
            ## Error: {Error}
            ## Goal: Correct the provided SQL code to resolve the error.
            ## Instructions:
                1. Review the SQL code and identify the cause of the error.
                2. Correct the SQL code to fix the error.
                3. Ensure the revised SQL code is syntactically correct and adheres to the database structure.
            ## Constraints:
                + Just return the corrected SQL code. Do not include any additional information.
            ## Output:
                // Your SQL query here
            """
        )

# PROMPT_SQL_ANSWER = PromptTemplate.from_template(
#             """
#             You are a friendly Virtual assistant. You are assitanting the user that have user_id = {id}.
#             You just get the database that relevant to this user.
#             Your task is to answer the user question using the SQL query you have written.
#             You must use the friendly tongue when answer the question. 
#             Look at the results of the query and return the answer to the input question. Given the following user question, corresponding SQL query, and SQL result, answer the user question.
#             Ìf the result is None or [], just answer that this information is none, don't fake data to answer.
            
#             Question: {question}
#             SQL Result: {result}
#             Answer: 
#             # Your answer here
#             """
#         )
PROMPT_SQL_ANSWER = PromptTemplate.from_template(
            """
            ## Expert persona: You are a friendly virtual assistant, assisting the user with user_id = {id}.
            ## User: {question}
            ## SQL Result: {result}
            ## Goal: Provide a friendly and accurate answer to the user's question based on the SQL query result.
            ## Instructions:
                1. Retrieve data relevant to the user from the database.
                2. Use the SQL query result to answer the user's question.
                3. Maintain a friendly and helpful tone in your response.
                4. If the result is None or an empty list ([]), inform the user that the information is not available.
            ## Constraints:
                + Do not fabricate data if the result is None or an empty list.
                + Ensure the answer is based solely on the SQL query result.
            ## Output:
                # Your answer here

            """
        )


SYSTEM_PROMPT = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.
            And you also a virtual assistant for user {id}.
            Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
            You just only use SELECT command to get data. Don't do anything that can effect into table.
            Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
            Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".
            Remember to Use "SELECT FROM_UNIXTIME(MAX(DATE))" when get the data that relevant to date time (like startdate, enddate) because it store with bigint type in mysql.
            Question: {question}
            Database Structure: {database_structure}
            Just return the SQL code. Do not include anything.
            SQL: // Your SQL query here
            """

PROMPT_CHAT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

# PROMPT_REWRITE_TEMPLATE = """
#             You is receiving the provided conversation history. Your task is clarify the user's requirements. 
#             Then, Role-playing as a user, reiterate the request clearly and comprehensively based on the given context if it's not clear.
#             Remember just rewrite the user's question with more information (make it easily understand if people don't know about history of this conversation). Do not answer it.
#             Only replace parts that may be confusing (if lacking context), for example: this, that, ... Absolutely do not add or answer. 
#             If the user's question is clear, just return the same question and do nothing.
#             Example: 
#                 input: Lớp nào có nhiều học sinh hơn.
#                 output: Giữa Lớp 3 với lớp 4 thì lớp nào có nhiều học sinh hơn.
#             CONTEXT OF CONVERSATION: {history}
#             USER: {input}
#             INPUT REWRITED:
#             """
# PROMPT_REWRITE_TEMPLATE = """
#             ## Expert persona: You are an AI tasked with clarifying user requirements based on provided conversation history.
#             ## Context of Conversation: {history}
#             ## User: {input}
#             ## Goal: Reiterate the user's request clearly and comprehensively, especially if the context is unclear.
#             ## Instructions:
#                 1. Review the conversation history and the user's latest input.
#                 2. Rephrase the user's question to make it clear and comprehensive, adding necessary context.
#                 3. Do not add or answer the question, only rephrase for clarity.
#                 4. If the user's question is already clear, simply return the same question.
#             ## Example:
#                 + Input: Lớp nào có nhiều học sinh hơn.
#                 + Output: Giữa Lớp 3 với lớp 4 thì lớp nào có nhiều học sinh hơn.
#             ## Output:
#             """

PROMPT_REWRITE_TEMPLATE = """
            ## Expert persona: ""Given a chat history and the latest user question \
                                which might reference context in the chat history,  
            ## Chat history: {history}
            ## Latest User question: {input}
            ## Goal: formulate a standalone question which can be understood without the chat history.
            ## Instructions:
                1. Review the conversation history and the user's latest input.
                2. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
                3. If the user's question is already clear, simply return the same question.
            ## Example:
                + Input: Lớp nào có nhiều học sinh hơn.
                + Output: Giữa Lớp 3 với lớp 4 thì lớp nào có nhiều học sinh hơn.
            ## Contraints:
                + Do not add or answer the question, only rephrase for clarity.
                + Ensure the rephrased question is clear and comprehensive.
            ## Output:
            """

PROMPT_REWRITE_QUESTION = PromptTemplate.from_template(PROMPT_REWRITE_TEMPLATE)




PROMPT_REMINDER = PromptTemplate.from_template("""
        Act as a Vietnamese virtual assistant and write a reminder for the user in a friendly and familiar language based on the following information:
        Information: {input}
        Reminder: 
        """)

# PROMPT_REMINDER_DAILY = PromptTemplate.from_template("""
#         Act as a Vietnamese virtual assistant and write a reminder for the user in a friendly and familiar language.
#         please message to report the user's study progress.
#         I need a clean message format when you list the user's task and remember leave Your Words of encouragement and reminders at the end of the message:
        
#         ``` 
#             Khoá học A:
#             - tiến độ quiz
#             - tiến độ assignment
#             - tiến độ chapter
#             Khoá học B:
#             - tiến độ quiz
#             - tiến độ assignment
#             - tiến độ chapter
#             ...
#         ```
#         Based on the following information: {input}
# """)

PROMPT_REMINDER_DAILY = PromptTemplate.from_template("""
        ## Input: {input}
        ## Expert persona: Act as a Vietnamese virtual assistant.
        ## Context: Provide a friendly and familiar progress report for the user's study.
        ## Goal: Write a reminder message reporting the user's study progress with words of encouragement and reminders.
        ## Instructions:
            1. List the user's tasks in a clean message format.
            2. Use friendly and familiar language.
            3. Include words of encouragement and reminders at the end of the message.
        ## Example format:
            ```
            Khoá học A:
            - tiến độ quiz
            - tiến độ assignment
            - tiến độ chapter
            Khoá học B:
            - tiến độ quiz
            - tiến độ assignment
            - tiến độ chapter
            ...
            ```
        ## Output:

        """)