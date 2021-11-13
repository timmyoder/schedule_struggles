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
    roster_id = pw.IntegerField(primary_key=True)
    user_id = pw.IntegerField(unique=True)
    display_name = pw.CharField()
    team_name = pw.CharField(null=True)


class Standings(BaseModel):
    user = pw.ForeignKeyField(Users,
                              field='roster_id',
                              backref='standings')
    week_1_rank = pw.IntegerField(null=True)
    week_2_rank = pw.IntegerField(null=True)
    week_3_rank = pw.IntegerField(null=True)
    week_4_rank = pw.IntegerField(null=True)
    week_5_rank = pw.IntegerField(null=True)
    week_6_rank = pw.IntegerField(null=True)
    week_7_rank = pw.IntegerField(null=True)
    week_8_rank = pw.IntegerField(null=True)
    week_9_rank = pw.IntegerField(null=True)
    week_10_rank = pw.IntegerField(null=True)
    week_11_rank = pw.IntegerField(null=True)
    week_12_rank = pw.IntegerField(null=True)
    week_13_rank = pw.IntegerField(null=True)
    week_14_rank = pw.IntegerField(null=True)


class Scores(BaseModel):
    user = pw.ForeignKeyField(Users,
                              field='roster_id',
                              backref='scores')
    week = pw.IntegerField()
    score = pw.FloatField()
    matchup_id = pw.IntegerField()

    class Meta:
        indexes = (
            (("user", "week"), True),
        )


class WeeklyResults(BaseModel):
    user = pw.ForeignKeyField(Users,
                              field='roster_id',
                              backref='week_results')
    week = pw.IntegerField()
    win_loss_tie = pw.CharField()
    total_score = pw.FloatField()


ALL_TABLES = [Users,
              Standings,
              Scores,
              WeeklyResults]


def clear_db():
    if db_file.exists():
        os.remove(db_file)
        logger.info('existing database deleted')
    with db.connection():
        db.create_tables(ALL_TABLES)
        logger.info('New db file create')


if __name__ == '__main__':
    clear_db()
