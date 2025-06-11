# database.py

from databases import Database

DATABASE_URL = "sqlite:///./test.db"  # برای حالت موقتی
database = Database(DATABASE_URL)

async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()

async def save_message(user_id: int, message: str):
    query = "INSERT INTO messages (user_id, message) VALUES (:user_id, :message)"
    values = {"user_id": user_id, "message": message}
    await database.execute(query=query, values=values)

async def init_db():
    # ساخت جدول در صورت نبود
    query = """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        message TEXT
    )
    """
    await database.execute(query)
