from contextlib import contextmanager


@contextmanager
def db_session():

    from emoji import db

    session = db.session()
    try:
        yield session
    except:
        session.rollback()
        session.close()
        raise

    try:
        session.commit()
    except:
        session.close()
        raise


class AppModel():
    """
    Mock the Django way of persisting models
    """
    @classmethod
    def create(cls, *args, **kwargs):
        with db_session() as db_sesh:
            new_model = cls(*args, **kwargs)
            db_sesh.add(new_model)
        return new_model

    def save(self):
        with db_session() as db_sesh:
            db_sesh.add(self)
        return self

    def delete(self):
        with db_session() as db_sesh:
            db_sesh.delete(self)
        return self
