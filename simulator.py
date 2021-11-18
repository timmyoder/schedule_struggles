import pandas as pd

from schedule import Schedule
from data_grabber import DataGrabber


class Simulator(Schedule, DataGrabber):
    def __init__(self, cur_week, n_runs=100000):
        Schedule.__init__(self)
        DataGrabber.__init__(self, cur_week=cur_week)

        self.wins = pd.DataFrame()
        self.n_runs = n_runs

        self.simple_wins = {}
        self.calc_simple_wins()
        self.sim_rank = self.simple_wins

    def score_game(self, matchup_tuple):
        pass

    def calc_simple_wins(self):

        for week in self.scores.keys():
            week_scores = self.scores[week]
            wins = week_scores['score'].rank() / len(week_scores)
            wins.name = 'week_wins'
            total_score = self.rank[week].set_index('user')[['display_name',
                                                             'team_name',
                                                             'total_score']]
            simple_wins = total_score.join(wins)
            if week == 1:
                simple_wins['wins'] = wins
            else:
                total_wins = self.simple_wins[week-1]['wins'] + wins
                simple_wins['wins'] = total_wins

            self.simple_wins[week] = simple_wins




if __name__ == '__main__':
    sim = Simulator(9)
