"""The whole shebang"""

from models import clear_db
import sleeper_scraper
import judge
from animator import RankAnimation
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s week_number",
        description="calculate win probabilities of fantasy football"
    )
    parser.add_argument('--week', 
                        help='current week to calculate scores')
    return parser


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()

    cur_week = int(args.week)
    print(f'Calculating for Week {cur_week}')
    clear_db()
    sleeper_scraper.main(cur_week=cur_week)
    judge.main(cur_week=cur_week)

    animator = RankAnimation(cur_week=cur_week)
    animator.animate_real()
    animator.animate_sim()
    print('gifs generated')
