import os

import peewee as pw
from loguru import logger
import pathlib

project_root = pathlib.Path(__file__).parent
db_file = project_root / 'ff.db'
db = pw.SqliteDatabase(db_file)


class BaseModel(pw.Model):
    class Meta:
        """required for each class"""
        database = db


class Users(BaseModel):
    small_id = pw.AutoField()
    user_id = pw.IntegerField(unique=True)
    display_name = pw.CharField()
    team_name = pw.CharField(null=True)


class Standings(BaseModel):
    week = pw.IntegerField(primary_key=True)
    place_1 = pw.IntegerField()
    place_2 = pw.IntegerField()
    place_3 = pw.IntegerField()
    place_4 = pw.IntegerField()
    place_5 = pw.IntegerField()
    place_6 = pw.IntegerField()
    place_7 = pw.IntegerField()
    place_8 = pw.IntegerField()
    place_9 = pw.IntegerField()
    place_10 = pw.IntegerField()
    place_11 = pw.IntegerField()
    place_12 = pw.IntegerField()


class Scores(BaseModel):
    user = pw.ForeignKeyField(Users,
                              field='small_id',
                              backref='scores')
    week = pw.IntegerField()
    score = pw.FloatField()

    class Meta:
        indexes = (
            (("user", "week"), True),
        )


ALL_TABLES = [Users,
              Standings,
              Scores]


def clear_db():
    if db_file.exists():
        os.remove(db_file)
        logger.info('existing database deleted')
    with db.connection():
        db.create_tables(ALL_TABLES)
        logger.info('New db file create')


if __name__ == '__main__':
    clear_db()
