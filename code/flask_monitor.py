import io
import random

import pandas as pd

from flask import Flask, render_template, Response

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

xs = None
ys = None
app = Flask(__name__)

@app.route('/plot.png')
def plot_png():
    fig = get_figure()
    plt.xticks(rotation=80)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

def get_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(xs, ys)
    axis.xaxis.set_major_locator(ticker.MultipleLocator(20))
    axis.set_ylabel("Moisture")
    axis.grid(True)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

@app.route('/')
def main():
    global xs, ys
    # Getting lines for rendering table
    lines = None
    with open("output.txt", "r") as f:
        lines = [l for l in f.readlines() if "LOG" in l]

    # Getting a DataFrame to generate plot
    df = pd.read_csv(io.StringIO("\n".join(lines)), sep=";")
    df.columns = ["date", "type", "relay", "moisture", "waterlevel"]

    # Filter for when the sensor is out the water
    df = df[df["waterlevel"] < 20]
    
    xs = list(df["date"])
    ys = list(df["moisture"])

    return render_template("data.html", lines=lines[::-1], last_line=lines[-1])
