import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime
from mpl_finance import candlestick_ochl as candlestick
style.use('ggplot')

class BitcoinTradingGraph:
    def __init__(self, df, title=None):
        self.df = df
        self.net_worths = np.zeros(len(df))
        fig = plt.figure()
        fig.suptitle(title)
        self.net_worth_ax = plt.subplot2grid((6, 1), (0, 0), rowspan=2, colspan=1)
        self.price_ax = plt.subplot2grid((6, 1), (2, 0), rowspan=8, colspan=1, sharex=self.net_worth_ax)
        plt.subplots_adjust(left=0.11, bottom=0.24,right=0.90, top=0.90, wspace=0.2, hspace=0)
        plt.show(block=False)

    def _render_net_worth(self, current_step, net_worth, step_range, dates):
        self.net_worth_ax.clear()
        self.net_worth_ax.plot_date(dates, self.net_worths[step_range], '-', label='Net Worth')
        self.net_worth_ax.legend()
        legend = self.net_worth_ax.legend(loc=2, ncol=2, prop={'size': 8})
        legend.get_frame().set_alpha(0.4)
        last_date = self.df['Timestamp'].values[current_step]
        last_net_worth = self.net_worths[current_step]
        self.net_worth_ax.annotate('{0:.2f}'.format(net_worth), (last_date, last_net_worth),
                                   xytext=(last_date, last_net_worth),
                                   bbox=dict(boxstyle='round',fc='w', ec='k', lw=1),
                                   color="black",
                                   fontsize="small")
        self.net_worth_ax.set_ylim(
            min(self.net_worths[np.nonzero(self.net_worths)]) / 1.25, max(self.net_worths) * 1.25)

    def _render_price(self, current_step, net_worth, step_range, dates):
        self.price_ax.clear()
        candlesticks = zip(dates,
                           self.df['Open'].values[step_range], self.df['Close'].values[step_range],
                           self.df['High'].values[step_range], self.df['Low'].values[step_range])
        candlestick(self.price_ax, candlesticks, width=20)
        last_date = self.df['Timestamp'].values[current_step]
        last_close = self.df['Close'].values[current_step]
        last_high = self.df['High'].values[current_step]

    def _render_trades(self, current_step, trades, step_range):
        for trade in trades:
            if trade['step'] in step_range:
                date = self.df['Timestamp'].values[trade['step']]
                close = self.df['Close'].values[trade['step']]
                high = self.df['High'].values[trade['step']]
                low = self.df['Low'].values[trade['step']]
                if trade['type'] == 'buy':
                    high_low = low
                    color = 'g'
                else:
                    high_low = high
                    color = 'r'
                total = '{0:.2f}'.format(trade['total'])
                self.price_ax.annotate('$' + str(total), (date, close),
                                       xytext=(date, high_low),
                                       bbox=dict(boxstyle='round',fc='w', ec='k', lw=1, alpha=0.4),
                                       color=color,
                                       alpha=0.4,
                                       fontsize="small")

    def render(self, current_step, net_worth, trades, window_size=40):
        self.net_worths[current_step] = net_worth
        window_start = max(current_step - window_size, 0)
        step_range = range(window_start, current_step + 1)
        dates = self.df['Timestamp'].values[step_range]
        self._render_net_worth(current_step, net_worth, step_range, dates)
        self._render_price(current_step, net_worth, step_range, dates)
        self._render_trades(current_step, trades, step_range)
        date_labels = np.array([datetime.utcfromtimestamp(x).strftime(
            '%Y-%m-%d %H:%M') for x in self.df['Timestamp'].values[step_range]])
        self.price_ax.set_xticklabels(
            date_labels, rotation=45, horizontalalignment='right')
        plt.setp(self.net_worth_ax.get_xticklabels(), visible=False)
        plt.pause(0.2)

    def close(self):
        plt.close()
