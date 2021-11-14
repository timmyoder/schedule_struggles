import pandas as pd
from peewee import fn

from models import Users, WeeklyResults, Scores, Standings


def df(query):
    return pd.DataFrame(list(query.dicts()))


class DataGrabber:
    def __init__(self, cur_week):
        self.cur_week = cur_week
        self.users = df(Users.select()).rename(
            columns={'roster_id': 'user'}).set_index('user')

        self.rank = {}
        self.scores = {}

        self.sim_rank = {}

        self.get_all_ranks(cur_week)
        self.get_all_scores(cur_week)

    def get_rank(self, week):
        rank_str = f'week_{week}_rank'
        q = Standings.select(Standings.user,
                             getattr(Standings, rank_str),
                             Users.display_name,
                             Users.team_name).join(Users)
        rank = df(q).sort_values(rank_str)
        rank[rank_str] += 1
        wins = df(WeeklyResults.select(WeeklyResults.user,
                                       fn.Count(WeeklyResults.win_loss_tie).alias('wins')
                                       ).where(
            (WeeklyResults.week <= week) & (WeeklyResults.win_loss_tie == 'W')
        ).group_by(WeeklyResults.user)).set_index('user')
        total_score = df(WeeklyResults.select(WeeklyResults.user,
                                              WeeklyResults.total_score
                                              ).where(
            (WeeklyResults.week == week)
        )).set_index('user')

        rank = rank.join(wins, on='user').join(total_score, on='user')

        rank = rank.fillna(0)

        self.rank[week] = rank

        return rank

    def get_all_ranks(self, cur_week):
        for week in range(1, cur_week + 1):
            self.get_rank(week)

    def get_scores(self, week):
        scores = df(Scores.select(Scores.user,
                                  Scores.score).where(
            Scores.week == week)).set_index('user')
        scores = scores.join(self.users['display_name'])
        self.scores[week] = scores

        return scores

    def get_all_scores(self, cur_week):
        for week in range(1, cur_week + 1):
            self.get_scores(week)


if __name__ == '__main__':
    d = DataGrabber(9)
