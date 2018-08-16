

from svglib.svglib import svg2rlg
import xml.dom.minidom
# Import of the canvas
from reportlab.pdfgen import canvas

# # Import of the renderer (image part)
from reportlab.graphics import renderPDF

def run(x=450,y=330,z=20,a=290):
	rlg = svg2rlg("./data/test3/Current_alpha_fig.svg")
	rlg.scale(0.8,0.8)
	c = canvas.Canvas("example3.pdf")
	# c.scale(0.5,0.5)
	# c.setTitle("my_title_we_dont_care")
	c.setPageSize((x, y))

#	# Generation of the first page
# 	# You have a last option on this function, 
# 	# about the boundary but you can leave it as default.
#	# renderPDF.draw(rlg, c, 0, 608)
# 	# renderPDF.draw(rlg, c, 60, 540 - rlg.height)
# 	# c.showPage()

# 	# Generation of the second page
	renderPDF.draw(rlg, c, z, a)
	c.showPage()

# 	# Save
	c.save()

