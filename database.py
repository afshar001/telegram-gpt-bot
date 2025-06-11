import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./messages.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

messages = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime, default=sqlalchemy.func.now()),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
