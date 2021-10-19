#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd
import os
import settings


class PlotView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        plotLayout = QVBoxLayout()
        #create plot widget
        self.plot = Plot()
        #add the plot toolbar and the canvas widgets to the plotLayout (toolbar above the canvas)
        plotLayout.addWidget(self.plot.toolbar)
        plotLayout.addWidget(self.plot.canvas)
        self.setLayout(plotLayout)

    def set_controller(self, controller):
        self.controller = controller

    def update(self, selected_table: pd.DataFrame) -> None:
        self.setup_update(selected_table)
        if selected_table.empty:
            print("Error! Filtered table EmptyDtaframe! No such combinations!")
        else:
            #sort by values (for legend)
            selected_table.sort_values(by=['bias','variance'], inplace=True)
            for index, row in selected_table.iterrows():
                path = f"{settings.BASE_DIR}/Simulation/Simulation_data/{row['file_name']}.csv"
                if os.path.exists(path):
                    data = pd.read_csv(path, header=None)
                    self.plot.add_line(row, data)
                else:
                    print(f"File {row['file_name']} does not exist!")
            #create plot legend and show plot
            self.plot.legend.create()
            self.plot.show()

    def setup_update(self, selected_table: pd.DataFrame) -> None:
        #clear plot
        self.plot.ax.clear()
        #setup plot legend and color generator
        self.legend = PlotLegend(self.plot)
        self.color = PlotColor(selected_table)
        self.plot.set_legend(self.legend)
        self.plot.set_color_generator(self.color)
        

class PlotLegend:
    def __init__(self, plot):
        self.plot = plot
        #legend constructing helper lists
        self.legend_labels=list()
        self.ax_label_lines=list()

    def update(self, row):
        #append line to list (needed for legend construction)
        self.ax_label_lines.append(self.plot.ax.lines[len(self.plot.ax.lines)-1])
        #define and append line label to lable list (needed for legend)
        label = f"bias = {row['bias']}, variance = {row['variance']}"
        self.legend_labels.append(label)

    def create(self):
        self.plot.ax.legend(self.ax_label_lines, self.legend_labels)


class PlotColor:
    def __init__(self, selected_table):
        #count variable for color pallete construction
        self.count = 0
        #number of data items/plot lines (needed for color pallete constructions)
        self.n_lines = len(selected_table)

    def generate(self):
        #line color
        plot_color = self.rgba_color(self.count, self.n_lines)
        self.count +=1
        return plot_color

    def rgba_color(self, n, N):
        import matplotlib
        #normalize item number values to colormap
        norm = matplotlib.colors.Normalize(vmin=0, vmax=N)
        #colormap possible values = viridis, jet, spectral
        return matplotlib.cm.jet(norm(n))


class Plot(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #construct matplotlib canvas and figure
        self.figure = Figure()
        self.ax = self.figure.add_subplot(211)
        self.ax.set(xlabel="time", ylabel="vesicle position")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumWidth(1000)
        #construct the Navigation toolbar widget (it takes the Canvas widget and a parent QMainWindow)
        self.toolbar = NavigationToolbar(self.canvas, self)

    def add_line(self, row, data: pd.DataFrame) -> None:
        #add line to plot
        self.ax.plot(data[0][:], data[1][:], color = self.color.generate())
        #update legend constructor
        self.legend.update(row)

    def set_legend(self, legend: PlotLegend):
        self.legend = legend

    def set_color_generator(self, color: PlotColor):
        self.color = color

    def show(self):
        self.canvas.draw()



