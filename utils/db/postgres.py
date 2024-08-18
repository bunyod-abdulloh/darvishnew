from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):

        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # ======================= TABLE | USERS =======================
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(100) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        fio VARCHAR(255) NULL,
        phone VARCHAR(30) NULL        
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def add_user_json(self, full_name, username, telegram_id, fio, phone):
        sql = "INSERT INTO users (full_name, username, telegram_id, fio, phone) VALUES($1, $2, $3, $4, $5)"
        return await self.execute(sql, full_name, username, telegram_id, fio, phone, fetchrow=True)

    async def updateuser_fullname(self, telegram_id, fio):
        sql = f"UPDATE users SET fio='{fio}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def updateuser_phone(self, telegram_id, phone):
        sql = f"UPDATE users SET phone='{phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def delete_user(self, telegram_id):
        await self.execute(f"DELETE FROM users WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_users(self):
        await self.execute("DROP TABLE users", execute=True)

    # ======================= TABLE | TABLES =======================
    async def create_table_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS medialar_tables (
        table_number INTEGER PRIMARY KEY NOT NULL,
        channel_id VARCHAR(50) NULL,
        comment TEXT NULL,
        files BOOLEAN DEFAULT FALSE
        );
        """
        await self.execute(sql, execute=True)

    async def select_all_tables(self, table_type):
        sql = f"SELECT * FROM medialar_tables WHERE table_type='{table_type}' ORDER BY table_number ASC"
        return await self.execute(sql, fetch=True)

    async def select_table_tables(self):
        sql = "SELECT * FROM medialar_tables"
        return await self.execute(sql, fetch=True)

    async def get_channel_id(self, table_number):
        sql = f"SELECT channel_id FROM medialar_tables WHERE table_number='{table_number}'"
        return await self.execute(sql, fetchrow=True)

    async def select_media_by_id(self, table_number):
        sql = f"SELECT * FROM medialar_tables WHERE table_number='{table_number}'"
        return await self.execute(sql, fetchrow=True)

    async def delete_table_tables(self, table_number):
        await self.execute(f"DELETE FROM medialar_tables WHERE table_number='{table_number}'", execute=True)

    async def drop_table_tables(self):
        await self.execute(f"DROP TABLE medialar_tables", execute=True)

    # ======================= TABLE | MEDIA =======================
    async def create_table_projects(self):
        sql = """
        CREATE TABLE IF NOT EXISTS medialar_table9 (
        id SERIAL PRIMARY KEY NOT NULL,
        sequence INTEGER NOT NULL,
        file_id VARCHAR(200) NULL,
        file_type VARCHAR(20) NULL,
        category VARCHAR(50) NOT NULL,
        subcategory VARCHAR(50) NOT NULL,
        caption TEXT NULL,
        link VARCHAR(200) NULL        
        );
        """
        await self.execute(sql, execute=True)

    async def add_projects(self, sequence, file_id, file_type, category, subcategory, caption):
        sql = ("INSERT INTO medialar_table9 (sequence, file_id, file_type, category, subcategory, caption) "
               "VALUES($1, $2, $3, $4, $5, $6)")
        return await self.execute(sql, sequence, file_id, file_type, category, subcategory, caption, fetchrow=True)

    async def select_all_media(self, table_name):
        sql = f"SELECT * FROM {table_name} ORDER BY lesson_number"
        return await self.execute(sql, fetch=True)

    async def select_all_projects(self):
        sql = "SELECT * FROM medialar_table9"
        return await self.execute(sql, fetch=True)

    async def select_projects(self):
        sql = """
        SELECT row_number() OVER () AS rank, category, id
        FROM (
            SELECT DISTINCT ON (category) category, id
            FROM medialar_table9
            ORDER BY category, id ASC
        ) subquery
        """
        return await self.execute(sql, fetch=True)

    async def select_project_name(self, id_):
        sql = f"SELECT * FROM medialar_table9 WHERE id='{id_}'"
        return await self.execute(sql, fetchrow=True)

    async def select_project_by_id(self, id_):
        sql = f"SELECT * FROM medialar_table9 WHERE id='{id_}'"
        return await self.execute(sql, fetchrow=True)

    async def select_project_by_categories(self, category_name):
        sql = f"SELECT * FROM medialar_table9 WHERE category='{category_name}' ORDER BY sequence ASC"
        return await self.execute(sql, fetch=True)

    async def select_all_articles(self):
        sql = f"SELECT * FROM medialar_table10 ORDER BY id"
        return await self.execute(sql, fetch=True)

    async def db_get_media_by_id(self, table_name, lesson_number):
        sql = f"SELECT * FROM {table_name} WHERE lesson_number='{lesson_number}'"
        return await self.execute(sql, fetchrow=True)

    async def drop_table_media(self, table_name):
        await self.execute(f"DROP TABLE {table_name}", execute=True)

    # ARTICLES

    async def add_articles(self, file_name, link):
        sql = "INSERT INTO medialar_table10 (file_name, link) VALUES($1, $2)"
        return await self.execute(sql, file_name, link, fetchrow=True)

    # ================== TESTLAR | YAXIN =================================
    async def create_table_testlaryaxin(self):
        sql = """
        CREATE TABLE IF NOT EXISTS testlar_nevrozyaxin (
        id SERIAL PRIMARY KEY,
        scale_type VARCHAR (50) NOT NULL,
        question TEXT NOT NULL,
        a VARCHAR(50) NOT NULL,
        b VARCHAR(50) NOT NULL,
        c VARCHAR(50) NOT NULL,
        d VARCHAR(50) NOT NULL,
        e VARCHAR(50) NOT NULL        
        );
        """
        await self.execute(sql, execute=True)

    async def add_questions_yaxin(self, scale_type, question, a, b, c, d, e):
        sql = ("INSERT INTO testlar_nevrozyaxin(scale_type, question, a, b, c, d, e) "
               "VALUES($1, $2, $3, $4, $5, $6, $7)")
        return await self.execute(sql, scale_type, question, a, b, c, d, e, fetchrow=True)

    async def drop_table_yaxin(self):
        await self.execute(f"DROP TABLE testlar_nevrozyaxin", execute=True)

    async def select_all_yaxin(self):
        sql = "SELECT * FROM testlar_nevrozyaxin ORDER BY id"
        return await self.execute(sql, fetch=True)

    # ======================= TABLE | YAXIN_SCALES =======================
    async def create_table_yaxinscales(self):
        sql = """
        CREATE TABLE IF NOT EXISTS yaxinscales (
        scale_type VARCHAR (50) NOT NULL,
        question_number INTEGER NULL,
        point_one FLOAT NULL,
        point_two FLOAT NULL,
        point_three FLOAT NULL,
        point_four FLOAT NULL,
        point_five FLOAT NULL        
        );
        """
        await self.execute(sql, execute=True)

    async def add_yaxin_scales(self, scale_type, question_number, point_one, point_two,
                               point_three, point_four, point_five):
        sql = ("INSERT INTO yaxinscales (scale_type, question_number, point_one, point_two, point_three, "
               "point_four, point_five) VALUES ($1, $2, $3, $4, $5, $6, $7)")
        return await self.execute(sql, scale_type, question_number, point_one, point_two, point_three,
                                  point_four, point_five, fetchrow=True)

    async def select_question_scale(self, scale_type, question_number):
        sql = f"SELECT * FROM yaxinscales WHERE scale_type='{scale_type}' AND question_number='{question_number}'"
        return await self.execute(sql, fetchrow=True)

    async def drop_table_yaxinscales(self):
        await self.execute(f"DROP TABLE yaxinscales", execute=True)

    # ======================= TABLE | YAXIN_TEMPORARY =======================
    async def create_table_temporaryyaxin(self):
        sql = """
        CREATE TABLE IF NOT EXISTS temporaryyaxin (
        id SERIAL PRIMARY KEY,
        created_at DATE DEFAULT CURRENT_DATE,        
        fullname VARCHAR(255) NULL,
        phone VARCHAR(30) NULL,
        telegram_id BIGINT NOT NULL,
        test_type VARCHAR(50) NOT NULL,
        scale_type VARCHAR(50) NULL,
        question_number INTEGER NULL,
        answer NUMERIC NULL                
        );
        """
        await self.execute(sql, execute=True)

    async def addyaxinfullname_temporary(self, telegram_id, fullname):
        sql = "INSERT INTO temporaryyaxin (telegram_id, fullname) VALUES ($1, $2)"
        return await self.execute(sql, telegram_id, fullname, fetchrow=True)

    async def addyaxinphone_temporary(self, telegram_id, phone):
        sql = f"UPDATE temporaryyaxin SET phone='{phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def add_yaxin_temporary(self, telegram_id, test_type, scale_type, question_number, answer):
        sql = ("INSERT INTO temporaryyaxin (telegram_id, test_type, scale_type, question_number, answer) "
               "VALUES ($1, $2, $3, $4, $5)")
        return await self.execute(sql, telegram_id, test_type, scale_type, question_number, answer, fetchrow=True)

    async def select_datas_temporary(self, telegram_id, scale_type):
        sql = (f"SELECT ROUND(SUM(answer), 2)  FROM temporaryyaxin WHERE telegram_id='{telegram_id}' "
               f"AND scale_type='{scale_type}'")
        return await self.execute(sql, fetchval=True)

    # async def get_answers_temporary(self, telegram_id, scale_type):
    #     sql = (f"SELECT * FROM temporaryyaxin WHERE telegram_id='{telegram_id}' "
    #            f"AND scale_type='{scale_type}'")
    #     return await self.execute(sql, fetch=True)

    async def back_user_yaxintemporary(self, telegram_id, question_number):
        await self.execute(f"DELETE FROM temporaryyaxin WHERE telegram_id='{telegram_id}' "
                           f"AND question_number='{question_number}'", execute=True)

    async def delete_user_yaxintemporary(self, telegram_id):
        await self.execute(f"DELETE FROM temporaryyaxin WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_temporaryyaxin(self):
        await self.execute(f"DROP TABLE temporaryyaxin", execute=True)

    # ======================= TABLE | YAXIN_ANSWERS =======================
    async def create_table_yaxinanswers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS yaxinanswers (
        id SERIAL PRIMARY KEY,
        date_created DATE DEFAULT CURRENT_DATE,
        full_name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL,
        test_type VARCHAR(50) NOT NULL,
        scale_type VARCHAR(50) NULL,
        all_points NUMERIC NULL                        
        );
        """
        await self.execute(sql, execute=True)

    async def add_yaxinanswers(self, full_name, telegram_id, test_type, scale_type, all_points):
        sql = ("INSERT INTO yaxinanswers (full_name, telegram_id, test_type, scale_type, all_points) "
               "VALUES ($1, $2, $3, $4, $5)")
        return await self.execute(sql, full_name, telegram_id, test_type, scale_type, all_points, fetchrow=True)

    async def delete_user_yaxinanswers(self, telegram_id):
        await self.execute(f"DELETE FROM yaxinanswers WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_yaxinanswers(self):
        await self.execute(f"DROP TABLE yaxinanswers", execute=True)

    # ======================= TABLE | AYZENK_TEMPERAMENT =======================
    async def create_table_ayztempquestions(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ayztempquestions (
        id SERIAL PRIMARY KEY,                  
        question_number INTEGER NOT NULL,           
        question TEXT NOT NULL                                    
        );
        """
        await self.execute(sql, execute=True)

    async def add_ayztempquestion(self, question_number, question):
        sql = "INSERT INTO ayztempquestions (question_number, question) VALUES ($1, $2)"
        return await self.execute(sql, question_number, question, fetchrow=True)

    async def select_questions_ayztemp(self):
        sql = f"SELECT * FROM ayztempquestions ORDER BY (question_number)"
        return await self.execute(sql, fetch=True)

    # ======================= TABLE | AYZENK_SCALES =======================
    async def create_table_ayztempscales(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ayztempscales (  
        id SERIAL PRIMARY KEY,              
        scale_type VARCHAR(50) NOT NULL,       
        yes INTEGER NOT NULL,           
        no_ INTEGER NOT NULL                                    
        );
        """
        await self.execute(sql, execute=True)

    async def add_ayztempscales(self, scale_type, yes, no_):
        sql = "INSERT INTO ayztempscales (scale_type, yes, no_) VALUES ($1, $2, $3)"
        return await self.execute(sql, scale_type, yes, no_, fetchrow=True)

    async def get_yes_ayzscales(self, yes):
        sql = f"SELECT scale_type FROM ayztempscales WHERE yes={yes}"
        return await self.execute(sql, fetchrow=True)

    async def get_no_ayzscales(self, no_):
        sql = f"SELECT scale_type FROM ayztempscales WHERE no_='{no_}'"
        return await self.execute(sql, fetchrow=True)

    # ======================= TABLE | AYZENK_TEMP =======================
    async def create_table_ayztemptemp(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ayztemptemp (
        created_at DATE DEFAULT CURRENT_DATE,  
        telegram_id BIGINT NOT NULL,              
        scale_type VARCHAR(50) NULL,
        question_number INTEGER NULL,       
        yes INTEGER NULL,           
        no_ INTEGER NULL                                    
        );
        """
        await self.execute(sql, execute=True)

    async def add_ayztemptempyes(self, telegram_id, scale_type, question_number, yes):
        sql = "INSERT INTO ayztemptemp (telegram_id, scale_type, question_number, yes) VALUES ($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, scale_type, question_number, yes, fetchrow=True)

    async def add_ayztemptempno(self, telegram_id, scale_type, question_number, no_):
        sql = "INSERT INTO ayztemptemp (telegram_id, scale_type, question_number, no_) VALUES ($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, scale_type, question_number, no_, fetchrow=True)

    async def select_sum_ayztemptempyes(self, telegram_id, scale_type):
        sql = f"SELECT SUM(yes) FROM ayztemptemp WHERE telegram_id='{telegram_id}' AND scale_type='{scale_type}'"
        return await self.execute(sql, fetchrow=True)

    async def select_check_ayztemptemp(self, telegram_id, question_number):
        sql = (f"SELECT * FROM ayztemptemp WHERE telegram_id='{telegram_id}' AND "
               f"question_number='{question_number}'")
        return await self.execute(sql, fetchrow=True)

    async def select_sum_ayztemptempno(self, telegram_id, scale_type):
        sql = f"SELECT SUM(no_) FROM ayztemptemp WHERE telegram_id='{telegram_id}' AND scale_type='{scale_type}'"
        return await self.execute(sql, fetchrow=True)

    async def back_user_ayztemptemp(self, telegram_id, question_number):
        await self.execute(f"DELETE FROM ayztemptemp WHERE telegram_id='{telegram_id}' "
                           f"AND question_number='{question_number}'", execute=True)

    async def delete_ayztemptemp(self, telegram_id):
        await self.execute(f"DELETE FROM ayztemptemp WHERE telegram_id='{telegram_id}'", execute=True)

    # ======================= TABLE | LEONGARD_QUESTIONS =======================
    async def create_table_leoquestions(self):
        sql = """
        CREATE TABLE IF NOT EXISTS leoquestions (                          
        question_number INTEGER NOT NULL,                   
        question TEXT NOT NULL                                            
        );
        """
        await self.execute(sql, execute=True)

    async def add_leoquestions(self, question_number, question):
        sql = "INSERT INTO leoquestions (question_number, question) VALUES ($1, $2)"
        return await self.execute(sql, question_number, question, fetchrow=True)

    async def select_questions_leo(self):
        sql = f"SELECT * FROM leoquestions ORDER BY (question_number)"
        return await self.execute(sql, fetch=True)

    # ======================= TABLE | LEONGARD_SCALES =======================
    async def create_table_leoscales(self):
        sql = """
        CREATE TABLE IF NOT EXISTS leoscales (                          
        id SERIAL PRIMARY KEY,
        scale_type VARCHAR(15) NOT NULL,        
        yes INTEGER NULL,
        no_ INTEGER NULL                                    
        );
        """
        await self.execute(sql, execute=True)

    async def add_leoscales(self, scale_type, yes, no_):
        sql = "INSERT INTO leoscales (scale_type, yes, no_) VALUES ($1, $2, $3)"
        return await self.execute(sql, scale_type, yes, no_, fetchrow=True)

    async def get_yes_leoscales(self, yes):
        sql = f"SELECT scale_type FROM leoscales WHERE yes={yes}"
        return await self.execute(sql, fetchrow=True)

    async def get_no_leoscales(self, no_):
        sql = f"SELECT scale_type FROM leoscales WHERE no_='{no_}'"
        return await self.execute(sql, fetchrow=True)

    # ======================= TABLE | LEONGARD_TEMPORARY =======================
    async def create_table_leotemp(self):
        sql = """
        CREATE TABLE IF NOT EXISTS leotemp (
        created_at DATE DEFAULT CURRENT_DATE,  
        telegram_id BIGINT NOT NULL,              
        scale_type VARCHAR(50) NULL,
        question_number INTEGER NULL,       
        yes INTEGER DEFAULT 0,            
        no_ INTEGER DEFAULT 0                                                    
        );
        """
        await self.execute(sql, execute=True)

    async def add_leotemp(self, telegram_id, scale_type, question_number, yes, no_):
        sql = "INSERT INTO leotemp (telegram_id, scale_type, question_number, yes, no_) VALUES ($1, $2, $3, $4, $5)"
        return await self.execute(sql, telegram_id, scale_type, question_number, yes, no_, fetchrow=True)

    async def select_check_leotemp(self, telegram_id, question_number):
        sql = (f"SELECT * FROM leotemp WHERE telegram_id='{telegram_id}' AND "
               f"question_number='{question_number}'")
        return await self.execute(sql, fetchrow=True)

    async def get_sums_leotemp(self, telegram_id, scale_type):
        sql = (f"SELECT scale_type, SUM(yes) AS total_yes, SUM(no_) AS total_no "
               f"FROM leotemp "
               f"WHERE telegram_id = $1 AND scale_type = $2 "
               f"GROUP BY scale_type")
        return await self.execute(sql, telegram_id, scale_type, fetchrow=True)

    async def add_leotempyes(self, telegram_id, scale_type, question_number, yes):
        sql = "INSERT INTO leotemp (telegram_id, scale_type, question_number, yes) VALUES ($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, scale_type, question_number, yes, fetchrow=True)

    async def add_leotempno(self, telegram_id, scale_type, question_number, no_):
        sql = "INSERT INTO leotemp (telegram_id, scale_type, question_number, no_) VALUES ($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, scale_type, question_number, no_, fetchrow=True)

    async def delete_leotemp(self, telegram_id):
        await self.execute(f"DELETE FROM leotemp WHERE telegram_id='{telegram_id}'", execute=True)

    async def back_leotemp(self, telegram_id, question_number):
        await self.execute(f"DELETE FROM leotemp WHERE telegram_id='{telegram_id}' "
                           f"AND question_number='{question_number}'", execute=True)
