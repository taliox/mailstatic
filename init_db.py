from mailstatic.database import db_session, init_db
import os


if __name__ == '__main__':
    try:
        os.remove(os.path.join("/tmp", "test.db"))
    except OSError:
        pass

    init_db()
