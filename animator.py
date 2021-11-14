import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.ticker as ticker
from IPython.display import HTML
from data_grabber import DataGrabber


class RankAnimation(DataGrabber):
    def __init__(self, cur_week,
                 simulated_file_name='sim.gif',
                 real_file_name='real.gif'):
        super().__init__(cur_week)
        self.real_file = real_file_name
        self.sim_file = simulated_file_name
        self.fig, self.ax = plt.subplots(figsize=(12, 6))

    def plot_server(self, week):
        data_to_plot = self.rank[week+1]

        self.ax.clear()
        self.ax.barh(data_to_plot['display_name'], data_to_plot['wins'])
        self.ax.invert_yaxis()
        dx = data_to_plot['wins'].max() * .005

        for i, (wins, name, score) in enumerate(zip(data_to_plot['wins'],
                                                    data_to_plot['display_name'],
                                                    data_to_plot['total_score'])):
            self.ax.text(wins - dx, i, f'points:', size=10,
                         weight=600, ha='right', va='center')

            self.ax.text(wins + dx, i, f'{score:,.0f}', size=10, ha='left', va='center')

        self.ax.text(1, 0.4, f'Week {week+1}', transform=self.ax.transAxes,
                     color='tab:gray', size=30, ha='right', weight=800)

        self.ax.text(0, 1.06, 'Wins', transform=self.ax.transAxes,
                     size=12, color='tab:gray')
        self.ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        self.ax.xaxis.set_ticks_position('top')
        self.ax.tick_params(axis='x', colors='tab:grey', labelsize=12)
        self.ax.set_xlim(-.2, data_to_plot['wins'].max()+1)
        self.ax.margins(0, 0.01)
        self.ax.grid(which='major', axis='x', linestyle='-')
        self.ax.set_axisbelow(True)
        self.ax.text(0, 1.12, 'Simulated Rankings',
                     transform=self.ax.transAxes, size=24, weight=600, ha='left')
        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.box(False)
        plt.tight_layout()

    def animate_real(self):
        animator = animation.FuncAnimation(self.fig,
                                           self.plot_server,
                                           frames=self.cur_week,
                                           interval=1500,
                                           repeat=True,
                                           repeat_delay=2000)
        animator.save(self.real_file, writer='imagemagick')

    def animate_sim(self):
        animator = animation.FuncAnimation(self.fig,
                                           self.plot_server,
                                           frames=self.cur_week,
                                           interval=1500,
                                           repeat=True,
                                           repeat_delay=2000)
        animator.save(self.real_file, writer='imagemagick')


if __name__ == '__main__':
    a = RankAnimation(9)
    a.animate_real()
