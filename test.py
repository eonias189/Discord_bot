from data import db_session
from data.users import User

db_session.global_init("db/discord_bot.db")
db_sess = db_session.create_session()
print(db_sess.query(User).all())
