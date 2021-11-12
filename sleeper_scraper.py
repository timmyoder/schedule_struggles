import requests
from loguru import logger
import sleeper_wrapper as sw

from models import db, Users, Scores

LEAGUE_ID = 738137102939750400
SLEEPER_API = f'https://api.sleeper.app/v1/league/{LEAGUE_ID}'
MATCHUPS = f'{SLEEPER_API}/matchups'
USERS = f'{SLEEPER_API}/users'
league = sw.League(LEAGUE_ID)

roster_dict = league.map_rosterid_to_ownerid(league.get_rosters())
user_roster_dict = inv_map = {v: k for k, v in roster_dict.items()}


def populate_users():
    users = requests.get(USERS).json()
    logger.debug('Users retrieved')
    for user in users:
        user_id = user['user_id']
        display_name = user['display_name']
        try:
            team_name = user['metadata']['team_name']
        except KeyError:
            team_name = f'Team {display_name}'

        roster_id = user_roster_dict[user_id]

        user, created = Users.get_or_create(user_id=user_id,
                                            display_name=display_name,
                                            team_name=team_name,
                                            roster_id=roster_id)
        if created:
            logger.info(f'{display_name} add to db')


def populate_scores(cur_wk):
    for week in range(1, cur_wk+1):
        for match in league.get_matchups(cur_wk):
            roster_id = match['roster_id']
            score = match['points']
            matchup_id = match['matchup_id']

            with db.atomic():
                score, created = Scores.get_or_create(user_id=roster_id,
                                                      week=week,
                                                      score=score,
                                                      matchup_id=matchup_id)
                if created:
                    logger.info(f'Week {week} score added for user {roster_id}')
                else:
                    logger.debug(f'Week {week} score for user {roster_id} exists')


if __name__ == '__main__':
    populate_users()
    populate_scores(cur_wk=9)


