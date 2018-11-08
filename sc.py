import arcpy
import os
from math import ceil
import numpy as np


class SquareCover(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "SquareCover"
		self.description = "TO DO"
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		param0 = arcpy.Parameter(name = "in_lines",
		                         displayName = "Input Lines",
		                         direction = "Input",
		                         parameterType = "Required",
		                         datatype = "DEFeatureClass")
		param1 = arcpy.Parameter(name = "workspace",
		                         displayName = "Workspace",
		                         direction = "Input",
		                         parameterType = "Required",
		                         datatype = "DEWorkspace")
		param2 = arcpy.Parameter(name = "out_squares",
		                         displayName = "Output Squares",
		                         direction = "Input",
		                         parameterType = "Required",
		                         datatype = "GPString")					 

		param3 = arcpy.Parameter(name="overwrite_output",
		                         displayName="Overwrite Output",
		                         direction="Input",
		                         parameterType="Required",
		                         datatype="GPBoolean")
								 
								 
		param4 = arcpy.Parameter(name = "in_squares",
		                         displayName = "Square Templates",
		                         direction = "Input",
		                         parameterType = "Required",
		                         datatype = "DEFeatureClass")
		param3.value = True
		
		param0.value = r"Q:\User\Casey Meisenzahl\Square-Covering\SquareCoveringDB.gdb\line"
		param1.value = r"Q:\User\Casey Meisenzahl\Square-Covering\SquareCoveringDB.gdb"
		param2.value = r"output"
		param4.value = r"Q:\User\Casey Meisenzahl\Square-Covering\SquareCoveringDB.gdb\Square"
		
		params = [param0, param1, param2, param3, param4]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.	This method is called after internal validation."""
		return

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		in_lines = parameters[0].valueAsText
		workspace = parameters[1].valueAsText
		out_feature = parameters[2].valueAsText
		in_squares = parameters[4].valueAsText
		
		out_squares = os.path.join(workspace, out_feature)
		
		length = 100
		arcpy.env.overwriteOutput = parameters[3].value
		
		out_mem = "in_memory/out"
		
		sr = arcpy.Describe(in_squares).spatialReference
		arcpy.CreateFeatureclass_management("in_memory", "out", "POLYGON", template=in_squares, spatial_reference=sr)
		
		fields = arcpy.ListFields(in_lines)
		
		fields = map(lambda f: f.name, fields)

		if "SHAPE" in fields:
			fields.remove("SHAPE")
		elif "Shape" in fields:
			fields.remove("Shape")
			
		fields.insert(0, "SHAPE@")
		
		lines = list()
		
		with arcpy.da.SearchCursor(in_lines, fields) as scur:
			for srow in scur:
				line = srow[0]
				lines.append(line)

		with arcpy.da.InsertCursor(out_mem, ["SHAPE@"] ) as icur:
			for line in lines:
				squares = self.get_squares(line, length)
				for square in squares:
					icur.insertRow([square,])
						
		arcpy.CopyFeatures_management(out_mem, out_squares)
		arcpy.Delete_management(out_mem)
		
		return

	def get_squares(self, line, length):
		squares = list()
		angle = get_angle(line)
		arcpy.AddMessage(angle)
		x = line.firstPoint.X
		y = line.firstPoint.Y
		arcpy.AddMessage(line.firstPoint.X)
		arcpy.AddMessage(line.lastPoint.X)
		arcpy.AddMessage("  ")
		if angle < 45 and angle > -45:
			a = arcpy.Point(x-(length/2), y+length)
			b = arcpy.Point(x+(length/2), y+length)
			c = arcpy.Point(x+(length/2), y)
			d = arcpy.Point(x-(length/2), y)
			
			p = arcpy.Point(x-(length/2), y)
			q = arcpy.Point(x+(length/2), y)
			r = arcpy.Point(x+(length/2), y-length)
			s = arcpy.Point(x-(length/2), y-length)
			
			squares.append(arcpy.Polygon(arcpy.Array([a,b,c,d])))
			squares.append(arcpy.Polygon(arcpy.Array([p,q,r,s])))
		else:
			a = arcpy.Point(x-length, y+(length/2))
			b = arcpy.Point(x, y+(length/2))
			c = arcpy.Point(x, y-(length/2))
			d = arcpy.Point(x-length, y-(length/2))
			
			p = arcpy.Point(x+length, y+(length/2))
			q = arcpy.Point(x, y+(length/2))
			r = arcpy.Point(x, y-(length/2))
			s = arcpy.Point(x+length, y-(length/2))
			
			squares.append(arcpy.Polygon(arcpy.Array([a,b,c,d])))
			squares.append(arcpy.Polygon(arcpy.Array([p,q,r,s])))
		
		return squares

		
def get_angle(line):
	p1 = line.firstPoint
	p2 = line.lastPoint
	y = p1.Y-p2.Y
	x = p1.X-p2.X
	if x == 0:
		if y > 0:
			angle = np.pi/2
		else:
			angle = (-1)*np.pi/2
	else:
		angle = np.arctan(y/x)
	angle = np.degrees(angle)
	return angle
		
		