"""The whole shebang"""

from models import clear_db
import sleeper_scraper
import judge
from animator import RankAnimation

if __name__ == '__main__':
    cur_week = 10
    clear_db()
    sleeper_scraper.main(cur_week=cur_week)
    judge.main(cur_week=cur_week)

    animator = RankAnimation(cur_week=cur_week)
    animator.animate_real()
    animator.animate_sim()
