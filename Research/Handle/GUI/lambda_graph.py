import numpy as np
import matplotlib.pyplot as plt
2lilifrom matplotlib.widgets import Slider, Button, RadioButtons, Cursor
import math
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D
from math import sqrt
from matplotlib.widgets import AxesWidget
import six
import pdb

class lambda_graph :
	def __init__(self, pointer) :
		self.pointer = pointer
		