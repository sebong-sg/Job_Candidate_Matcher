import sqlite3
try:
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📊 Database tables:", [t[0] for t in tables])
    
    # Check job counts
    cursor.execute("SELECT COUNT(*) FROM embedding_metadata WHERE key='title';")
    job_count = cursor.fetchone()[0]
    print(f"📁 Jobs in database: {job_count}")
    
    conn.close()
    print("✅ Database structure is healthy")
except Exception as e:
    print(f"❌ Database error: {e}")
