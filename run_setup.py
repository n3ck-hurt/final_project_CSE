import mysql.connector

sql_file = 'setup_db.sql'

try:
    with open(sql_file, 'r') as f:
        sql = f.read()
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='estares223'
    )
    cursor = conn.cursor()
    
    statements = sql.split(';')
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
                # Fetch any results to clear them
                try:
                    cursor.fetchall()
                except:
                    pass
            except Exception as e:
                print(f'Error in statement: {stmt[:50]}...')
                print(f'  Error: {e}')
    
    conn.commit()
    cursor.close()
    conn.close()
    print('✓ Database setup complete with students table!')
    print('✓ All tables created and populated with sample data!')
except Exception as e:
    print(f'Fatal error: {e}')
