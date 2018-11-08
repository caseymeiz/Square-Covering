import arcpy
import sc
reload(sc)
from sc import SquareCover

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "SquareCovering"
		self.alias = "sc"
		# List of tool classes associated with this toolbox
		self.tools = [SquareCover,]
