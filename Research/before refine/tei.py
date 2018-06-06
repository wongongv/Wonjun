import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters

plt = pg.plot(np.arange(10))
img = pg.exporters.ImageExporter(plt.plotItem)
img.export()