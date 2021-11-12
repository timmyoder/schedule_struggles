import pandas as pd
import numpy as numpy
from loguru import logger
import peewee as pw

from models import db, Users, Scores, WeeklyResults, Standings


def get_total_scores(week):
    total_score = Scores.select(Scores.user,
                                pw.fn.SUM(Scores.score).alias('total_score')
                                ).where(
        (Scores.week <= week)
    ).group_by(Scores.user).execute()

    score_dict = {}
    for user in total_score:
        score_dict[user.user.roster_id] = user.total_score

    return score_dict


def determine_games(week):
    for matchup in range(1, 7):
        match_query = Scores.select(Scores.user,
                                    Scores.score).where(
            (Scores.week == week) &
            (Scores.matchup_id == matchup)
        )
        match = pd.DataFrame(list(match_query.dicts()))
        if len(match['score'].unique()) == 1:
            match['result'] = 'T'
        else:
            winner_id = match['score'].idxmax()
            match.loc[winner_id, 'result'] = 'W'
            match.loc[match['result'].isna(), 'result'] = 'L'

        log_result(week, match)


def log_result(week, match):
    total_scores = get_total_scores(week=week)

    for ind, row in match.iterrows():
        with db.atomic():
            user = row['user']
            total_score = total_scores[user]
            try:
                WeeklyResults.get_or_create(user=user,
                                            week=week,
                                            win_loss_tie=row['result'],
                                            total_score=total_score)
                logger.info(f'Week {week} result for {user} added')
            except pw.IntegrityError:
                logger.debug(f'Week {week} result for {user} exists')


if __name__ == '__main__':
    for wk in range(2, 10):
        determine_games(wk)
