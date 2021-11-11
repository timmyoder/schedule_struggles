import requests
from loguru import logger

from models import db, Users

LEAGUE_ID = 738137102939750400
SLEEPER_API = f'https://api.sleeper.app/v1/league/{LEAGUE_ID}'
MATCHUPS = f'{SLEEPER_API}/matchups'
USERS = f'{SLEEPER_API}/users'

week_num = 1

r = requests.get(f'{MATCHUPS}{week_num}')


def populate_users():
    users = requests.get(USERS).json()
    logger.debug('Users retrieved')
    for user in users:
        user_id = user['user_id']
        display_name = user['display_name']
        try:
            team_name = user['metadata']['team_name']
        except KeyError:
            team_name = None

        user, created = Users.get_or_create(user_id=user_id,
                                            display_name=display_name,
                                            team_name=team_name)
        if created:
            logger.info(f'{display_name} add to db')


if __name__ == '__main__':
    populate_users()

