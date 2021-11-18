import numpy as np


class Schedule:
    # each team plays every other team once
    # each team plays once and only once a week
    def __init__(self, rng_seed=420):
        self.rng = np.random.default_rng(rng_seed)
        self.schedule = None
        self.create_schedule()

    @staticmethod
    def _next_table(table):
        """a table is a simple list of teams"""
        return [table[0]] + [table[-1]] + table[1:-1]
        # [0 1 2 3 4 5 6 7] -> [0 7 1 2 3 4 5 6]

    @staticmethod
    def _pairing_from_table(table):
        """ a pairing is a list of pairs of teams"""
        return list(zip(table[:len(table) // 2], table[-1:len(table) // 2 - 1:-1]))
        # [0 1 2 3 4 5 6 7] -> [(0,7), (1,6), (2,5), (3,4)]

    def round_robin(self, table):
        """a team is an element of the table"""
        pairing_list = []
        for day in range(len(table) - 1):
            pairing_list.append(self._pairing_from_table(table))
            table = self._next_table(table)
        return pairing_list

    def create_schedule(self):
        team_list = list(range(1, 13))
        self.rng.shuffle(team_list)
        first_11 = self.round_robin(team_list)
        rand_repeat = self.rng.choice(list(range(11)), 3)
        full_schedule = first_11 + [first_11[wk] for wk in rand_repeat]
        schedule = {}
        for key, value in enumerate(full_schedule):
            schedule[key+1] = value
        self.schedule = schedule

    def print(self):
        for week in self.schedule.keys():
            print(f'Week {week}: {self.schedule[week]}')

    def new_schedule(self):
        self.create_schedule()


if __name__ == '__main__':
    s = Schedule()
    s.print()