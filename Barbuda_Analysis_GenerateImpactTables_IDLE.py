########################################################################################################
# This document records the automated generation of impact analysis for Barbuda
# This takes the polygon layers of classified inundation for Barbuda
# 
# These layers are processed to tables of impact value as the intersection between the feature and the gridcode.

########################################################################################################

########################################################################################################
#
# Output is for each an impact table for each layer
############################################################################################################

##############################################################################################################
# Works in ArcMap (ArcCatalogue throws a licencing error!)
# Make sure that the folders are empty and the output geodatabase only has the inner buffer and coastline 
# Run on a clean Arc Catalogue
# Developing 25/03/2020
############################################################################################################
import arcpy

InputLayerGeoDataBase = r"D:\Cefas\A&B\InundationTables\CoastalVulnerabilityBarbuda_20200323.gdb"
OutputLayerGeoDataBase = r"D:\Cefas\A&B\InundationTables\CoastalImpactTables_Barbuda.gdb"
OutputCSVFileFolder = r"D:\Cefas\A&B\InundationTables\BarbudaCSVFiles"

# Set the default database
arcpy.env.workspace = InputLayerGeoDataBase
arcpy.env.scratchWorkspace = OutputLayerGeoDataBase
SpRef = arcpy.SpatialReference("WGS 1984 UTM Zone 20N")

#############################################
# For development 
arcpy.env.overwriteOutput = True
###########################################

# Set variable look ups

ImpactLayers = ["INF_BBQ_Roads_2020_84",
				"INF_BBQ_Helipads_hotosm",
				"INF_BBQ_FerryTerminal_polygon_hotosm",
				"INF_BBQ_FerryTerminal_point_hotosm",
				"INF_BBQ_Buildings_schools_hotosm",
				"INF_BBQ_Buildings_govt_hotosm",
				"INF_BBQ_Buildings_ALL_hotosm",
				"INF_BBQ_Airports_hotosm",
				"HDR_BBQ_Waterbodies_polygon_hotosm",
				"HDR_BBQ_Lagoons_2019_84",
				"SOC_BBQ_CulturalHeritage_2018_84",
				"PRT_BBQ_Sanctuary_2013_84",
				"TER_BBQ_KeyBiodiversityAreas_2020_84"]

ImpactLayerClassList = ["ID;type;name",
						"osm_id",
						"osm_id;amenity",
						"osm_id;amenity", 
						"osm_id",
						"osm_id;addrstreet;name",
						"osm_id;building",
						"osm_id;name",
						"osm_id;natural;water",
						"OBJECTID;Name",
						"Id;Site",
						"SC_ID;NAME",
						"SitRecID;NatName"]

############################################################################
#
# Obtain the impact information using the Tabulate intersection
############################################################################

############################################################################
# Loop through each impact layer and create the intersection table
#############################################################################
for Table in xrange(len(ImpactLayers)):
	# Get the cross tabulation values and output the results as a table
	InZoneFeatures = "Barbuda_FINAL_InundationClass_NEWDTM_PolygonV1"
	OuputTable = "Barbuda_InundationTable_" + ImpactLayers[Table]

	SUM_FIELDS = ""
	ImpactTable = arcpy.TabulateIntersection_analysis(	in_zone_features = InZoneFeatures, 
														zone_fields = "gridcode", 
														in_class_features = ImpactLayers[Table], 
														out_table = OuputTable,  
														class_fields = ImpactLayerClassList[Table],  
														sum_fields = SUM_FIELDS,  
														xy_tolerance = "-1 Unknown",  
														out_units = "UNKNOWN")
	# Output the table as csv file for further processing
	arcpy.TableToTable_conversion(in_rows = ImpactTable, 
												out_path = OutputCSVFileFolder,
												out_name = OuputTable + ".csv") 
	arcpy.Delete_management(ImpactTable)
################################################################################
# Successful 25/02/20 and rerun 27/03/20 but to changes to the polygons
# 
################################################################################
