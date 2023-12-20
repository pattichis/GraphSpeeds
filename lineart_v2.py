from __future__ import print_function

# Interactive visualization command in Jupyter Lab
# !pip install ipywidgets

import cv2
import os

from ipywidgets import interact, interactive, fixed, interact_manual, FloatSlider
import ipywidgets as widgets

import numpy as np              # import NumPy library

import numbers

# Plot the function:
import matplotlib.pyplot as plt

import math # for floor and ceiling
import sympy as sp
x = sp.symbols('x')

import pygame
import sys
import time

# Import plotly
# !pip install kaleido

import plotly
import plotly.graph_objects as go
import plotly.express as px

# Data frames using pandas
import pandas as pd

from IPython.display import HTML
from base64 import b64encode



def f(m, b):
  # Get the figure and axes handles
  fig, ax = plt.subplots()

  # X-axis
  minX  = -10 # minimum value for X
  maxX  = +10 # maximum value for Y
  xdata = range(minX, maxX+1, 1) # Integer points to plot
  plt.xlim(minX, maxX) # Set the x-limits for the plot
  fig.set_figwidth((maxX-minX)/2.0)

  # Y-axis
  minY  = -5  # minimum value for Y
  maxY  = +5  # maximum value for Y
  ydata = range(minY, maxY+1, 1) # Integer grid to display
  plt.ylim(minY, maxY) # Set the y-limits for the plot
  fig.set_figheight((maxY-minY)/2.0)


  # Define the grid over integer values:
  ax.set_xticks(xdata)
  ax.set_yticks(ydata)
  plt.grid(True, alpha=0.5) # Make opacity softer

  # Plot the two axes and add tick points:
  plt.axvline(x=0.0, ymin=minY, ymax=maxY) # x-axis
  plt.axhline(y=0.0, xmin=minX, xmax=maxX) # y-axis

  # Plot the integer tick points for x:
  tick_min = 0.5 - 0.25*1/(maxY - minY) # fraction for min Y
  tick_max = 0.5 + 0.25*1/(maxY - minY) # fraction for max Y
  for x_tick in range(minX, 0, 1):
    plt.axvline(x=x_tick, ymin=tick_min, ymax=tick_max)
    plt.text(x=x_tick-0.25, y=-0.75, s=str(x_tick), fontsize=12)

  for x_tick in range(1, maxX+1, 1):
    plt.axvline(x=x_tick, ymin=tick_min, ymax=tick_max)
    plt.text(x=x_tick-0.25, y=-0.75, s=str(x_tick), fontsize=12)

  plt.text(x=-0.5, y=-0.5, s="0", fontsize=12)
  plt.text(x=maxX/2.0, y=-1.5, s="x", fontsize=12)

  # Plot the integer tick points for y:
  tick_min = 0.5 - 0.25*1/(maxX - minX) # fraction for min X
  tick_max = 0.5 + 0.25*1/(maxX - minX) # fraction for max X
  for y_tick in range(minY, 0, 1):
    plt.axhline(y=y_tick, xmin=tick_min, xmax=tick_max)
    plt.text(y=y_tick-0.25, x=-1.0, s=str(y_tick), fontsize=12)

  for y_tick in range(1, maxY+1, 1):
    plt.axhline(y=y_tick, xmin=tick_min, xmax=tick_max)
    plt.text(y=y_tick-0.25, x=-1.0, s=str(y_tick), fontsize=12)

  plt.text(y=maxY/2.0, x=-2.0, s="y", fontsize=12)

  # remove the outside tick axes:
  ax.set_xticklabels([])
  ax.set_yticklabels([])


  # Plot the points:
  for x in xdata:
    y = m*x + b
    plt.plot(x, y, "ro")
  yall = m*np.linspace(minX, maxX, maxX-minX+1)+b
  plt.plot(xdata, yall, color="red")

  # Equation legend:
  plt.legend([str("y = "+str(m)+"*x+"+str(b))], edgecolor="red")

  # Manually set the legend color
  leg = ax.get_legend()
  leg.legendHandles[0].set_color('red')

  # Set the figure size:
  # plt.figure(figsize=(15, 15))
  plt.title("y=m*x+b", fontsize=14)

  plt.show()


# Create the interactive visualization code class.
import collections
class cuteGraph:
    """
    The cuteGraph class is used for graphing linear functions:
        y = m*x + b
    The class uses integer limits for x.

    Common Attributes
    -----------------
    m: the slope of the line to plot.
    b: the y-intercept of the line for x=0.

    minX: minimum value for X. Default=-10.
    maxX: maximum value for X. Default=+10.

    minY: minimum value for Y. Default=-5.
    maxY: maximum value for Y. Default=+5.

    gridDisplay:   True if displaying the grid. False if not.
    legendDisplay: True if displaying the legend. False if not.


    color: "red", "green", "blue", "olive", "cyan", "brown", etc.
    See colors at the website below:
    https://matplotlib.org/3.1.0/gallery/color/named_colors.html


    Common Methods
    --------------
    plotGraph():           Builds a graph with the defaults.
    setX(minX, maxX):      Sets the integer bounds for X.
    setY(minY, maxY):      Sets the integer bounds for Y.

    line(m, b, color):  Adds a line y=m*x+b.
    point(x, y, color): Adds a point (x, y).

    lineSeg(x1, y1, x2, y2, color):   Adds line segment (x1, y1) to (x2, y2)
    rectangle(x1, y1, x2, y2, color): Add rectange with corners (x1, y1), (x2, y2).

    plotAll(): Generate the plot for everything.
    """

    def __init__(self):
        """ Creates a graph object with default parameters.
        """

        # Create the named tuples data structures:
        self.LineVal    = collections.namedtuple('line',  ['m', 'b', 'color'])
        self.HLineVal   = collections.namedtuple('hline', ['yvalue', 'color'])
        self.PointVal   = collections.namedtuple('point', ['x', 'y', 'color'])
        self.RectVal    = collections.namedtuple('rect',     ['x1', 'y1', 'x2', 'y2', 'color'])
        self.LineSegVal = collections.namedtuple('lineseg',  ['x1', 'y1', 'x2', 'y2', 'color'])

        # Create the lists:
        self.Lines    = []
        self.HLines   = []
        self.Points   = []
        self.Rects    = []
        self.LineSegs = []
        
        # Line and point widths:
        self.line_width  = 2
        self.point_width = 2

        # X-axis, Y-axis: use integer values.
        self.setStep(step=1, stepPixels=20)
        self.setX (minX=-10, maxX=+10)
        self.setY (minY=-5, maxY=+5)

        # Setup the grid, legend, and axis visibility
        self.gridDisplay   = True
        self.legendDisplay = True
        self.axisVis = True

        # Setup everything for plotly:
        self.fig = go.Figure()

    # Setup a square grid
    def setStep(self, step, stepPixels):
      self.step = step
      self.stepPixels = stepPixels

    # Grid options
    def gridOn(self):
      self.gridDisplay = True

    def gridOff(self):
      self.gridDisplay = False
      
    def prepVideo(self, minX, minY, maxX, maxY, magFactor):
      self.setStep(step=1.0, stepPixels=20)
      
      Dx = magFactor*(maxX - minX)
      Dy = magFactor*(maxY - minY)
      
      centerX = (maxX + minX)/2.0
      centerY = (maxY + minY)/2.0
      
      minX = centerX - Dx/2.0
      maxX = centerX + Dx/2.0
      self.setX(minX=minX, maxX=maxX)
      
      minY = centerY - Dy/2.0
      maxY = centerY + Dy/2.0
      self.setY(minY=minY, maxY=maxY)
      
      # Turn off the extras before setting up the grid:
      self.allOff()
      
      # Prepare the grid
      self.setupGrid()
      
      # Main house
      self.setwidths(linewidth=5, pointwidth=2)


    # Legend options
    def legendOn(self):
      self.legendDisplay = True

    def legendOff(self):
      self.legendDisplay = False

    def axisOff(self):
      self.axisVis = False

    def allOff(self):
      self.gridOff()
      self.legendOff()
      self.axisOff()

    def addText(self, x, y, text, color):
      self.fig.add_annotation(
          x=x, y=y,
          text=text,  
          showarrow=False,
          align="center",
          font=dict(
            family="Courier New, monospace",
            size=16,
            color=color
            )
          )


    # .png, .jpeg, .svg, .pdf
    def saveImage(self, filename):
      """ saveImage(filename) saves filename.ext where ext=png, jpeg, svg, pdf
      """
      self.fig.write_image(filename, engine="kaleido", scale=1.0)

    # String representation for print() and debugging
    def __repr__(self) -> str:
      str_rep  = "CuteGraph class\n"
      str_rep += "MinX, MaxX, MinY, MaxY = "+str(self.minX)+", "+str(self.maxX)
      str_rep += ", "+str(self.minY)+", "+str(self.maxY)+"\n"
      str_rep += "Pixels width, height = "+str(self.width)+", "+str(self.height)
      str_rep += "Lines:"+str(self.Lines)+"\n"
      str_rep += "Horizontal Lines:"+str(self.HLines)+"\n"
      str_rep += "Points:"+str(self.Points)+"\n"
      str_rep += "Rectangles:"+str(self.Rects)+"\n"
      str_rep += "Line segments:"+str(self.LineSegs)+"\n"
      return str_rep

    def setX(self, minX, maxX):
      """ sets minimum and maximum values for x.
      """
      width = (maxX - minX + self.step) / self.step * self.stepPixels
      if (width <= 2048):
        self.minX  = minX
        self.maxX  = maxX
        self.width = width
      else:
        print("ERROR in setX(): too many pixels!")
        print("stepPixels="+str(self.stepPixels)+" is too large!")
        print("Width="+str(width)+" pixels > 1024")


    def setY(self, minY, maxY):
      """ sets minimum and maximum integer values for Y.
      """
      height = (maxY - minY + self.step) / self.step * self.stepPixels
      if (height <= 2048):
        self.minY  = minY
        self.maxY  = maxY
        self.height = height
      else:
        print("ERROR in setY(): too many pixels!")
        print("stepPixels="+str(self.stepPixels)+" is too large.")
        print("height="+str(height)+" pixels > 1024")


    def line(self, m, b, color):
      """ Adds a line with slope=m and y-intercept=b.
          Uses color to plot the line.
      """
      self.Lines.append(self.LineVal(m=m, b=b, color=color))

    def hline(self, yvalue, color):
      """ Adds a horizontal line with y=yvalue.
          Uses color to plot the line.
      """
      self.HLines.append(self.HLineVal(yvalue=yvalue, color=color))

    def point(self, x, y, color):
      """ Add a point with coordinates (x, y).
          Uses color to plot the point.
      """
      self.Points.append(self.PointVal(x=x,y=y, color=color))

    def rect(self, x1, y1, x2, y2, color):
      """ Add a rectangle with coordinates (x1, y1) and (x2, y2).
          Uses color to plot the point.
      """
      self.Rects.append(self.RectVal(x1=x1, y1=y1, x2=x2, y2=y2, color=color))

    def lineseg(self, x1, y1, x2, y2, color):
      """ Add a line segment with points (x1, y1) and (x2, y2).
          Uses color to plot the point.
      """
      self.LineSegs.append(self.LineSegVal(x1=x1, y1=y1, x2=x2, y2=y2, color=color))

    def setwidths(self, linewidth, pointwidth):
      self.line_width  = linewidth
      self.point_width = pointwidth

    def setupGrid(self, xdigits=3, xdecimals=0, ydigits=3, ydecimals=0, grid_color='red'):
      """ builds the grid using grid_color.
      """

      # X-axis
      minX = self.minX
      maxX = self.maxX
      numSamples = int((maxX-minX)/self.step)+1
      self.xdata = np.linspace(minX, maxX, numSamples)

      # Y-axis
      minY = self.minY
      maxY = self.maxY
      numSamples = int((maxY-minY)/self.step)+1
      self.ydata = np.linspace(minY, maxY, numSamples)

      # Plotly express figure ranges with grid:
      self.fig.update_yaxes(range=[minY, maxY],
                            showgrid=self.gridDisplay,
                            gridwidth=1,
                            gridcolor=grid_color,
                            scaleanchor = "x", scaleratio = 1,
                            automargin=False)
      self.fig.update_xaxes(range=[minX, maxX],
                            showgrid=self.gridDisplay,
                            gridwidth=1,
                            gridcolor=grid_color,
                            automargin=False)

      # Use plotly express layout for updates:
      self.fig.update_layout(xaxis = dict(
                              tickmode = 'linear',
                              tick0 = minX,
                              dtick = self.step
                                ),
                             yaxis = dict(
                                tickmode = 'linear',
                                tick0 = minY,
                                dtick = self.step
                                ),
                             height=self.height,
                             width=self.width,
                             autosize=False
                             )

      # Plot the two axes and add tick points:
      if (self.axisVis):
        self.fig.add_hline(y=0.0) # x-axis
        self.fig.add_vline(x=0.0) # y-axis

      # Update
      # self.fig.show()

    def plotAll(self):
      """ plots all defined lines and points.
      """

      # Plot Everything:
      for i in range(len(self.Points)):
        self.plotPoint(self.Points[i])

      for i in range(len(self.Lines)):
        self.plotLine(self.Lines[i])

      for i in range(len(self.Rects)):
        self.plotRect(self.Rects[i])

      for i in range(len(self.LineSegs)):
        self.plotLineSeg(self.LineSegs[i])
      
      for i in range(len(self.HLines)):
        self.plotHLine(self.HLines[i])

      # Setup the title for all of them:
      if (self.axisVis):
        self.fig.update_layout(
          title="Plots",
          xaxis_title="X",
          yaxis_title="Y",
          legend_title="List",
          font=dict(
            family="Courier New, monospace",
            size=12,
            color="RebeccaPurple"
          ))

      # Update the legend:
      self.fig.update_layout(showlegend=self.legendDisplay)

      # x axis visibility
      self.fig.update_xaxes(visible=self.axisVis)

      # y axis visibility
      self.fig.update_yaxes(visible=self.axisVis)

      # Update the graph:
      self.fig.show()

    def plotPoint(self, PointVal):
      """ plots a single point (x, y) using line_color
      """
      x_point, y_point, color = PointVal.x, PointVal.y, PointVal.color
      
      self.fig.add_trace(go.Scatter(
          x=[x_point], y=[y_point],
          marker=dict(size=18,
                      color=color,
                      line=dict(width=self.point_width,
                                color=color)),
          marker_color=color,
          marker_symbol="x",
          name="Point ("+str(x_point)+" ,"+str(y_point)+")",
          mode="markers"))

    def plotLine(self, LineVal):
      """ plots a single line given m, b, and line_color
      """
      m, b, line_color = LineVal.m, LineVal.b, LineVal.color

      # Do not support zoom-in:
      numpoints = 2
      xall = np.linspace(self.minX, self.maxX, numpoints)
      yall = m*xall + b

      # Use a simple name for the plot:
      if b>0:
        name_str = str("y = "+str(m)+"*x+"+str(b))
      elif b==0:
        name_str = str("y = "+str(m)+"*x")
      else:
        name_str = str("y = "+str(m)+"*x"+str(b))

      # Add the line plot:
      self.fig.add_trace(go.Scatter(
          x=xall,
          y=yall,
          mode="lines+markers",
          name=name_str,
          line=dict(color=line_color, width=self.line_width)))

    def plotHLine(self, HLineVal):
      """ plots a horizontal line y=yval using color
      """
      yvalue, color = HLineVal.yvalue, HLineVal.color
      self.fig.add_hline(y=yvalue,
          name="y="+str(yvalue),
          line_color=color, line_width=self.line_width)

    def plotLineSeg(self, LineSegVal):
      """ plots a line segment between two points
      """
      x1, x2, y1, y2 = LineSegVal.x1, LineSegVal.x2, LineSegVal.y1, LineSegVal.y2
      line_color = LineSegVal.color

      xall = [x1, x2]
      yall = [y1, y2]
      
      # Add the line plot:
      name_str  = "Line segment ("
      name_str += str(x1)+", "+str(y1)
      name_str += ") to ("+str(x2)+", "+str(y2)+")"
      self.fig.add_trace(go.Scatter(
          x=xall,
          y=yall,
          mode="lines+markers",
          name=name_str,
          line=dict(color=line_color, width=self.line_width)))

    def plotRect(self, RectVal):
      """ plots a rectangle given two corner points.
      """
      x1, x2, y1, y2 = RectVal.x1, RectVal.x2, RectVal.y1, RectVal.y2
      line_color = RectVal.color
      
      name_str  = "Rect: line ("
      name_str += str(x1)+", "+str(y1)
      name_str += ") to ("+str(x1)+", "+str(y2)+")"
      self.fig.add_trace(go.Scatter(
          x=[x1, x1],
          y=[y1, y2],
          mode="lines+markers",
          name=name_str,
          line=dict(color=line_color, width=self.line_width)))

      name_str  = "Rect: line ("
      name_str += str(x2)+", "+str(y1)
      name_str += ") to ("+str(x2)+", "+str(y2)+")"
      self.fig.add_trace(go.Scatter(
          x=[x2, x2],
          y=[y1, y2],
          mode="lines+markers",
          name=name_str,
          line=dict(color=line_color, width=self.line_width)))

      name_str  = "Rect: line ("
      name_str += str(x1)+", "+str(y1)
      name_str += ") to ("+str(x2)+", "+str(y1)+")"
      self.fig.add_trace(go.Scatter(
          x=[x1, x2],
          y=[y1, y1],
          mode="lines+markers",
          name=name_str,
          line=dict(color=line_color, width=self.line_width)))

      name_str  = "Rect: line ("
      name_str += str(x1)+", "+str(y2)
      name_str += ") to ("+str(x2)+", "+str(y2)+")"
      self.fig.add_trace(go.Scatter(
          x=[x1, x2],
          y=[y2, y2],
          mode="lines+markers",
          name=name_str,
          line=dict(color=line_color, width=self.line_width)))


def timer(seconds):
    # Increase to delay the loop
    watch_speed_factor = 2
    
    adjusted_seconds = seconds / watch_speed_factor
    time.sleep(adjusted_seconds)
    
class table(cuteGraph):
  def __init__(self, x = None, y = None, 
               img_path = None, img_loc = None, 
               img_speed = None):
    super().__init__()

    # Input arugments validation      
    if x is not None and y is not None:
      if len(x) != len(y):
        raise ValueError('Number of columns should be' /
                       'equal to number of column labels')
        
      if x is not list or y is not list:
        raise ValueError('Table inputs should be formated as lists')
      
      for column_lables in x:
        if not isinstance(column_lables, str):
          raise ValueError('Column lables should be strings')
      
      for data_values in y:
        if not isinstance(data_values, numbers.Number):
          raise ValueError('Data values should be numbers')
        
      self.column_labels = x
      self.data_values = y
    else:
      self.column_labels = []
      self.data_values = []
    
    if img_path is not None:
      if not isinstance(img_path, str):
        raise ValueError('path to image should be string')
      
      self.img_path = img_path
    else:
      self.img_path = []
    
    if img_loc is not None:
      if not isinstance(img_loc[0], numbers.Number) and  not isinstance(img_loc[1], numbers.Number):
        raise ValueError('Image location should be a number')
      
      if img_loc[0] > 0 and img_loc[1] > 0:
        raise ValueError('Image location should be non negative')
      
      self.img_loc = img_loc
    else:
      self.img_loc = (0, 0)
    
    if img_speed is not None:
      if img_speed < 1 or not isinstance(x, numbers.Number):
        raise ValueError('Speed should be number more than 1')
      
      self.img_speed = img_speed
    else:
      self.img_speed = 0
  
  def plotTable(self):
      """ plots a table from given columns
      """
      # Clear figure
      self.fig.data = []

      # Clear layout
      self.fig.layout = {}

      # Add the table plot
      self.fig.add_trace(go.Table(header=dict(values = self.column_labels), cells = dict(values = self.data_values)) )
      
      # Update the layout
      self.fig.update_layout(autosize = False)

      # Update the figure:
      self.fig.show()
  

def plotTablesLines(tables = None, fig_title = 
                    None, x_label = None, y_label = None, 
                    legend_title = None, legend_labels = None,
                    equation_labels = None):
    """ plots a table as plot from given columns
    """
  
    if fig_title is not None:
      if not isinstance(fig_title, str):
        raise ValueError('Figure title should be a string')
    
    if x_label is not None:
      if not isinstance(x_label, str):
        raise ValueError('X label should be a string')
    
    if y_label is not None:
      if not isinstance(y_label, str):
        raise ValueError('Y label should be a string')
    
    if legend_title is not None:
      if not isinstance(legend_title, str):
        raise ValueError('Legened label should be a string')
    
    if legend_labels is not None:
      for equation in legend_labels:
        if not isinstance(equation, str):
          raise ValueError('Equations should be a string')
      
      if len(legend_labels) != len(tables):
        raise ValueError('Numbers of labels must be equal to number of tables')
    
    # Clear figure data
    tmp = table()
    tmp.fig.data = []

    # Set the plotting parameters
    tmp.setStep(step=5, stepPixels=50)
    tmp.setY(minY=0,  maxY= 50)
    tmp.setX(minX=0, maxX= 50)
    tmp.setwidths(linewidth=2, pointwidth=3)
    tmp.setupGrid()
    
    
    # Overlay multiple plots in a figure
    if tables is not None:

      for tbl_idx, tbl in enumerate(tables):
        
        # Line equations
        if legend_labels is not None:
          tbl_name = legend_labels[tbl_idx]
        else:
          tbl_name = []
        
        # Adding plots onto existing figure
        tmp.fig.add_trace( go.Scatter(x = tbl.data_values[0], 
                                          y = tbl.data_values[1], 
                                          mode='lines+markers', 
                                          name = tbl_name) )
      
      # Update the figure layout with titles
      tmp.fig.update_layout(title=
                                {'text': fig_title,
                                    'y':0.9,
                                    'x':0.4,
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                },
                                xaxis_title= x_label,
                                yaxis_title= y_label,
                                legend_title= legend_title,
                                font=
                                dict(
                                  family="Courier New, monospace",
                                  size=13,
                                  color="RebeccaPurple"
                                  )
                                )
      
    # Update the layout
    tmp.fig.update_layout(autosize = False)

    # Update the figure
    tmp.fig.show()

def race(tables = None, vid_width = None, 
         vid_height = None, vid_title = None, 
         end_line_scale = None, end_line_color = None, 
         disp_font_sz = None, img_names = None, 
         img_size = None, fps = None):

      # Video dimension check
      if vid_width is not None:
        if vid_width <= 0 or not isinstance(vid_width, numbers.Number):
          raise ValueError('video width should be a postive number')
      else:
        # Default video width
        vid_width = 800 

      if vid_height is not None:
        if vid_height <= 0 or not isinstance(vid_height, numbers.Number):
          raise ValueError('video height should be a postive number')
      else:
        # Default video height
        vid_height = 600
      
      if fps is not None:
        if fps <= 0 or not isinstance(fps, numbers.Number):
          raise ValueError('Video fps should be a postive number')
      else:
        fps = 10
      
      # Video to store pygame
      out_vid = cv2.VideoWriter('out_vid.mp4',cv2.VideoWriter_fourcc(*"mp4v"), fps, (vid_width, vid_height))
      
      # Set pygame display with video dimensions
      vid_disp = pygame.display.set_mode((vid_width, vid_height))
      
      # pygame.display.set_caption('Race to Bumpers') # Enable this to run locally
      
      # Initialize pygame 
      pygame.init()
      
      # Video title check
      if vid_title is not None:
        if not isinstance(vid_title, str):
          raise ValueError('Video title should be string')
      else:
        # Default Name
        vid_title = 'Race'
      
      # Stop line check
      if end_line_scale is not None:
        if end_line_scale >=1 or end_line_scale <= 0 or not isinstance(end_line_scale, numbers.Number):
          raise ValueError('end line scale should between 0 and 1')
      else:
        # Default value
        end_line_scale = 0.3
      
      # Stop line color
      if end_line_color is not None:
        for color_value in end_line_color:
          if not isinstance(color_value, numbers.Number):
            raise ValueError('Colors should be numbers')
      else:
        # Red color
          end_line_color = (255, 0, 0)
      
      # Font size check
      if disp_font_sz is not None:
        if not isinstance(disp_font_sz, int):
          raise ValueError('Font size should be integer')
      else:
        # Default value 
        disp_font_sz = 25
      
      # Image Resize dimensions
      if img_size is not None:
        if not isinstance(img_size[0], numbers.Number) and  not isinstance(img_size[1], numbers.Number):
          raise ValueError('Image size should be a number')
      
        if img_size[0] <= 0 and img_size[1] <= 0:
          raise ValueError('Image location should be postive')
      else:
        # Default size
        img_size = (100, 100)
        
      if img_names is not None:
        if len(img_names) != len(tables):
          raise ValueError('Numbers of labels must be equal to number of tables')
        
        for img_name in img_names:
          if not isinstance(img_name, str):
            raise ValueError('Image names should be strings')
      else:
        img_names = []
      
      
      # Stop line 
      end_line = vid_width - end_line_scale*vid_width
      end_line_start = (end_line, 0)
      end_line_end = (end_line, vid_height)
      
      # Axis units
      axis_unit = 10
      axis_line = vid_height - 0.1*vid_height
      dist_axis = (0, axis_line)
      axis_font_sz = 15
      
      # Black color
      black = (0, 0, 0)
      
      # Video character font size
      vid_disp_font = pygame.font.Font(None, disp_font_sz)
      
      # Extract table objects attributes
      py_imgs = []
      py_rects = []
      py_rect_speed = []
      
      for tbl in tables:
        
        py_img = pygame.image.load(tbl.img_path)
        py_img = pygame.transform.scale(py_img, img_size)
        
        py_rect = pygame.Rect(tbl.img_loc[0], tbl.img_loc[1], 
                              py_img.get_width(), py_img.get_height())
      
        py_imgs.append(py_img)
        py_rects.append(py_rect)
        py_rect_speed.append(tbl.img_speed)

      # clock counter
      race_clock = 0
      break_time = 0
      
      while True:
        # Uncomment to run locally
        # for event in pygame.event.get():
        #   if event.type == pygame.QUIT:
        #     pygame.quit()
        #     sys.exit()
        
        # Fill display with white color
        vid_disp.fill((255, 255, 255))
                
        race_clock += 1
        
        # Slow down loop by increase number 
        timer(0.25)
        
        # Update pygame display for each table 
        for py_idx, py_rect in enumerate(py_rects):
          
          # Nulify image speed once reaching stop line
          if py_rect.right >= end_line:
            tables[py_idx].img_speed = 0
            py_rect_speed[py_idx] = 0
          
          vid_disp.blit(py_imgs[py_idx], py_rect)
          
          # Update rectangle at image speed
          py_rect.move_ip([tables[py_idx].img_speed, 0])
          
          # Overlay image name on video display
          img_name = vid_disp_font.render(f"{img_names[py_idx]}", True, (0, 0, 0))
          img_name_rect = img_name.get_rect()
          img_name_rect.topleft = (end_line + 50, py_rect.y)
          vid_disp.blit(img_name, img_name_rect)
          
          # Overlay image distance on video display
          dist = vid_disp_font.render(f"Distance: {py_rect.x} m", True, (0, 0, 0))
          dist_rect = dist.get_rect()
          dist_rect.topleft = (end_line + 50, py_rect.y + 20)
          vid_disp.blit(dist, dist_rect)
          
          # Overlay image speed on video display 
          spd = vid_disp_font.render(f"Speed:     {py_rect_speed[py_idx]} m/sec", True, (0, 0, 0))
          spd_rect = spd.get_rect()
          spd_rect.topleft = (end_line + 50, py_rect.y + 40)
          vid_disp.blit(spd, spd_rect)
          
          
        # Overlay clock time on video display
        race_timer = vid_disp_font.render(f"Time:       {race_clock} sec", True, (0, 0, 0))
        race_timer_rect = race_timer.get_rect()
        race_timer_rect.topleft = (end_line + 50, py_rects[-1].y + 100)
        vid_disp.blit(race_timer, race_timer_rect)
        
        # Overlay video title
        vid_title_ = vid_disp_font.render(f"{vid_title}", True, (0, 0, 0))
        vid_title_rect = vid_title_.get_rect()
        vid_title_rect.topleft = (end_line + 50, 10)
        vid_disp.blit(vid_title_, vid_title_rect)
        
        # Draw stop line and bottom line
        pygame.draw.line(vid_disp, end_line_color, end_line_start, end_line_end, 1)  
        pygame.draw.line(vid_disp, black, (0, axis_line), (end_line, axis_line), 1)
        
        # Update entire pygame display
        pygame.display.flip()

        # Save pygame display as video 
        cv2_img = pygame.surfarray.array3d(vid_disp)
        cv2_img = cv2_img.transpose([1, 0, 2])
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        out_vid.write(cv2_img)
        
        # Wait and break after reaching stop line        
        if sum(py_rect_speed) == 0:
          break_time +=1
          if break_time >= 3:
            out_vid.release()
            break
      

      # return "out_vid.mp4"
        

from skimage import io

def CreateVideo(video_name, file_list, fps):
  #self.plot_to_frame()
  height_list  = []
  width_list   = []
  video_frames = []

  # Find the biggest sizes
  for frame in file_list:
    img = io.imread(frame)
    video_frames.append(img)
    height, width, channels = img.shape
    height_list.append(height)
    width_list.append(width)

  #print(height_list)
  h_video=np.max(height_list)
  w_video=np.max(width_list)

  #fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
  video = cv2.VideoWriter(video_name,
            cv2.VideoWriter_fourcc(*'MJPG'),
            fps,
            (w_video, h_video))

  for frame in video_frames:
    video = padding(frame, video, h_video, w_video)

  video.release()

  vid = MakeVideo(video_name, width=w_video, height=h_video)
  return vid.HTML_str

def padding(frame, video, h_video, w_video):
  old_h, old_w, channels = frame.shape
  if divmod(h_video - old_h, 2)[1] != 0:
    pad_h_t = int((h_video - 1 - old_h) /2)
    pad_h_b = int((h_video + 1 - old_h) /2)

  else:
    pad_h_t = int((h_video - old_h) /2)
    pad_h_b = int((h_video - old_h) /2)

  if divmod(w_video - old_w, 2)[1] != 0:
    pad_w_l = int((w_video - 1 - old_w) /2)
    pad_w_r = int((w_video + 1 - old_w) /2)

  else:
    pad_w_l = int((w_video - old_w) /2)
    pad_w_r = int((w_video - old_w) /2)

  padding_image = cv2.copyMakeBorder(frame,
    pad_h_t, pad_h_b,
    pad_w_l, pad_w_r,
    cv2.BORDER_CONSTANT,
    None,
    value = [255, 255, 255])

  new_h, new_w, channels = padding_image.shape

  #plt.imshow(padding_image)
  #plt.show()
  padding_image = cv2.cvtColor(padding_image, cv2.COLOR_BGR2RGB)
  video.write(padding_image)
  return video


class MakeVideo:
  def __init__(self, mp4_fname, width, height):
    """ compresses the video file and displays in Jupyter notebook.
        mp4_fname represents the filename of the mp4 video.
    """
    self.mp4_fname = mp4_fname
    self.width  = width
    self.height = height

    # Compress file
    temp_file = "temp_video.mp4"
    self.compress(temp_file)

    # Create HTML for video display
    self.HTML_vid(temp_file)

  def compress(self, compressed_fname):
    """ compresses the given video file to compressed_finame
        If the filename is found, it replaces it with the current filename.
    """
    # Remove the compressed file name:
    if os.path.exists(compressed_fname):
      os.remove(compressed_fname)

    # Use ffmpeg to compress
    mp4_str = f"ffmpeg -i {self.mp4_fname} -vcodec libx264 {compressed_fname}"
    os.system(mp4_str)
    print("Compressed "+ self.mp4_fname + " into " + compressed_fname)

  def HTML_vid(self, compressed_fname):
    """ displays the compressed file in Juyter notebook.
    """
    mp4 = open(compressed_fname,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    self.HTML_str = """
                 <video width="%s" height="%s" controls loop autoplay>
                    <source src="%s" type="video/mp4">
                 </video> """ % (self.width, self.height, data_url)
