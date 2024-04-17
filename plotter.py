# Some parts of code were taken from
# https://matplotlib.org/stable/users/explain/animations/blitting.html
# (whole BlitManager class)

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from typing import NoReturn, List

plt.rcParams.update({'font.size': 7})


class BlitManager:
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for subclasses of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist
            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()


def plot_data(x: List[List[float]], y: List[List[float]], n: int) -> NoReturn:
    """
    Plots data

    Parameters
    ----------
    x: List[List[float]]
        X coords for each particle
    y: List[List[float]]
        Y coords for each particle
    n: int
        Frames amount
    """

    x_plot_data = [[],[]]
    y_plot_data = [[],[]]

    # Creating axes
    fig = plt.figure()
    gs = gridspec.GridSpec(1, 2, wspace=0.25, hspace=0.25)
    ax_static_anim = fig.add_subplot(gs[0, 0])
    ax_static = fig.add_subplot(gs[0, 1])

    # Setting up axes
    xlim_min = min(min(x[0]), min(x[1]))*1.1
    xlim_max = max(max(x[0]), max(x[1]))*1.1
    ylim_min = min(min(y[0]), min(y[1]))*1.1
    ylim_max = max(max(y[0]), max(y[1]))*1.1
    
    for ax in [ax_static_anim, ax_static]:
        # Limits
        ax.set_xlim([xlim_min, xlim_max])
        ax.set_ylim([ylim_min, ylim_max])

        # Labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.axhline(linewidth=0, c='black')
        ax.axvline(linewidth=0, c='black')

        # Major and minor ticks
        ax.xaxis.set_major_locator(MultipleLocator((xlim_max-xlim_min)/5))
        ax.yaxis.set_major_locator(MultipleLocator((ylim_max-ylim_min)/5))

        ax.xaxis.set_minor_locator(AutoMinorLocator(8))
        ax.yaxis.set_minor_locator(AutoMinorLocator(4))

        ax.grid(which='major', color='#CCCCCC', linestyle='--')
        ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    # Adding lines and frames text
    (line1,) = ax_static_anim.plot(x_plot_data[0], y_plot_data[0], animated=True, color='b')
    (line2,) = ax_static_anim.plot(x_plot_data[1], y_plot_data[1], animated=True, color='r')

    (line3,) = ax_static.plot(x[0], y[0], animated=False, color='b')
    (line4,) = ax_static.plot(x[1], y[1], animated=False, color='r')

    frame_numb = ax_static_anim.annotate(
        "0",
        (0, 1),
        xycoords="axes fraction",
        xytext=(10, -10),
        textcoords="offset points",
        ha="left",
        va="top",
        animated=True,
    )
    
    # Adding starting points on static plot
    ax_static.plot(x[0][0],y[0][0],'go', markersize=3, color='b') 
    ax_static.plot(x[1][0],y[1][0],'go', markersize=3, color='r') 


    bm = BlitManager(
        fig.canvas, 
        [
            line1,
            line2, 
            line3, 
            line4, 
            frame_numb
        ]
    )
    plt.show(block=False)
    plt.pause(.1)


    for i in range(n):
        x_plot_data[0].append(x[0][i])
        x_plot_data[1].append(x[1][i])

        y_plot_data[0].append(y[0][i])
        y_plot_data[1].append(y[1][i])


        line1.set_xdata(x_plot_data[0])
        line1.set_ydata(y_plot_data[0])
        line2.set_xdata(x_plot_data[1])
        line2.set_ydata(y_plot_data[1])

        frame_numb.set_text(f"frame: {i}")

        bm.update()
