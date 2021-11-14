import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.ticker as ticker
from data_grabber import DataGrabber


class RankAnimation(DataGrabber):
    def __init__(self, cur_week,
                 simulated_file_name='sim.gif',
                 real_file_name='real.gif'):
        super().__init__(cur_week)
        self.real_file = real_file_name
        self.sim_file = simulated_file_name
        self.fig, self.ax = plt.subplots(figsize=(12, 6))

    def plot_server(self, week, sim_or_real='real'):
        if sim_or_real == 'real':
            data_to_plot = self.rank[week + 1]
        else:
            data_to_plot = self.sim_rank[week + 1]
        self.ax.clear()

        # tableau colors
        colors = dict(zip(
            ['AuthenticEnigma', 'timmyoder', 'ryansradteam', 'theelectreon',
             'zacharyspecht', 'OmondiTDs', 'nmhemming', 'AEGD',
             'cheekykeeky', 'Footballisdeath', 'grcapoferri', 'habibis978'],
            [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
             (0.6823529411764706, 0.7803921568627451, 0.9098039215686274),
             (1.0, 0.4980392156862745, 0.054901960784313725),
             (1.0, 0.7333333333333333, 0.47058823529411764),
             (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
             (0.596078431372549, 0.8745098039215686, 0.5411764705882353),
             (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
             (1.0, 0.596078431372549, 0.5882352941176471),
             (0.5803921568627451, 0.403921568627451, 0.7411764705882353),
             (0.7725490196078432, 0.6901960784313725, 0.8352941176470589),
             (0.5490196078431373, 0.33725490196078434, 0.29411764705882354),
             (0.7686274509803922, 0.611764705882353, 0.5803921568627451),
             # (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),
             # (0.9686274509803922, 0.7137254901960784, 0.8235294117647058),
             # (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),
             # (0.7803921568627451, 0.7803921568627451, 0.7803921568627451),
             # (0.7372549019607844, 0.7411764705882353, 0.13333333333333333),
             # (0.8588235294117647, 0.8588235294117647, 0.5529411764705883),
             (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),
             (0.6196078431372549, 0.8549019607843137, 0.8980392156862745)]
        ))

        self.ax.barh(data_to_plot['display_name'], data_to_plot['wins'],
                     color=[colors[name]
                            for name in data_to_plot['display_name']])
        self.ax.invert_yaxis()
        dx = data_to_plot['wins'].max() * .005

        for i, (wins, name, score) in enumerate(zip(data_to_plot['wins'],
                                                    data_to_plot['display_name'],
                                                    data_to_plot['total_score'])):
            self.ax.text(wins - dx, i, f'points:', size=10,
                         weight=600, ha='right', va='center')

            self.ax.text(wins + dx, i, f'{score:,.0f}', size=10, ha='left', va='center')

        self.ax.text(1, 0.4, f'Week {week + 1}', transform=self.ax.transAxes,
                     color='tab:gray', size=30, ha='right', weight=800)

        self.ax.text(0, 1.06, 'Wins', transform=self.ax.transAxes,
                     size=12, color='tab:gray')
        self.ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        self.ax.xaxis.set_ticks_position('top')
        self.ax.tick_params(axis='x', colors='tab:grey', labelsize=12)
        self.ax.set_xlim(-.2, data_to_plot['wins'].max() + 1)
        self.ax.margins(0, 0.01)
        self.ax.grid(which='major', axis='x', linestyle='-')
        self.ax.set_axisbelow(True)
        self.ax.text(0, 1.12, f'{sim_or_real.capitalize()} Rankings',
                     transform=self.ax.transAxes, size=24, weight=600, ha='left')
        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        plt.box(False)
        plt.tight_layout()

    def animate_real(self):
        animator = animation.FuncAnimation(self.fig,
                                           self.plot_server,
                                           fargs=('real',),
                                           frames=self.cur_week,
                                           interval=1500,
                                           repeat=True,
                                           repeat_delay=2000)
        animator.save(self.real_file, writer='imagemagick')

    def animate_sim(self):
        animator = animation.FuncAnimation(self.fig,
                                           self.plot_server,
                                           fargs=('simulated',),
                                           frames=self.cur_week,
                                           interval=1500,
                                           repeat=True,
                                           repeat_delay=2000)
        animator.save(self.real_file, writer='imagemagick')


if __name__ == '__main__':
    a = RankAnimation(9)
    a.animate_real()
