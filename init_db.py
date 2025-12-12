#!/usr/bin/env python
import mysql.connector
from config import Config

try:
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        port=3306
    )
    cursor = conn.cursor()
    
    # Read SQL file
    with open('setup_db.sql', 'r') as f:
        sql_script = f.read()
    
    # Execute each statement
    for statement in sql_script.split(';'):
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
            except mysql.connector.Error as err:
                if err.errno == 1064:  # Syntax error
                    continue
                raise
    
    conn.commit()
    print('✓ Database setup complete!')
    
    # Verify tables
    cursor.execute('USE `sari-sari_store`')
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    print(f'✓ Tables: {", ".join(t[0] for t in tables)}')
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
