########################################################################################################
# This document records the automated generation of impact analysis for Antigua
# This takes the polygon layers of classified inundation for Antigua
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

InputLayerGeoDataBase = r"D:\Cefas\A&B\InundationTables\CoastalVulnerabilityAntigua_20200326.gdb"
OutputLayerGeoDataBase = r"D:\Cefas\A&B\InundationTables\CoastalImpactTables_Antigua.gdb"
OutputCSVFileFolder = r"D:\Cefas\A&B\InundationTables\AntiguaCSVFiles"

# Set the default database
arcpy.env.workspace = InputLayerGeoDataBase
arcpy.env.scratchWorkspace = OutputLayerGeoDataBase
SpRef = arcpy.SpatialReference("WGS 1984 UTM Zone 20N")

#############################################
# For development 
arcpy.env.overwriteOutput = True
###########################################

# Set variable look ups

ImpactLayers = ["ADM_ATG_Landmass_2005_84",
				"HDR_ATG_Waterbodies_2019_84",
				"INF_ATG_AccessRoad_APUA",
				"INF_ATG_Airports_hotosm",
				"INF_ATG_APUA_ElectricityWires",
				"INF_ATG_APUA_Substations",
				"INF_ATG_Buildings_2010_84",
				"INF_ATG_BusRoutes_2019_84",
				"INF_ATG_DamsReservoirs_APUA",
				"INF_ATG_EducationFacility",
				"INF_ATG_EVCharging_2019_84",
				"INF_ATG_FireStation",
				"INF_ATG_GasStations_2016_84",
				"INF_ATG_PoliceFacilities",
				"INF_ATG_PumpingStations_APUA",
				"INF_ATG_ReligiousCentres",
				"INF_ATG_SeaPorts_hotosm",
				"INF_ATG_WaterPipelines_APUA",
				"INF_ATG_WaterTanks_APUA",
				"INF_ATG_WaterTreatmentPlant_APUA",
				"INF_ATG_Wells_APUA",
				"PRT_ATG_BPNP_2019_84",
				"PRT_ATG_DevilsBridge_2010_84",
				"PRT_ATG_FortBarrington_2010_84",
				"PRT_ATG_GreenCastleHill_2010_84",
				"PRT_ATG_NelsonsDockyard_2010_84",
				"PRT_ATG_SMMA_2019_84",
				"SOC_ATG_Clinics_2016_84",
				"SOC_ATG_CulturalHeritage_2018_84",
				"SOC_ATG_EmergencyShelters_2019_84",
				"SOC_ATG_Schools_2017_84",
				"TER_ATG_KeyBiodiversityAreas_2020_84",
				"TER_ATG_LandCover_2010_84",
				"INF_ATG_NamedRoads_2016_84",
				"INF_ATG_MedicalFacilities",
				"hotosm_atg_buildings_polygons"]

ImpactLayerClassList = ["OBJECTID",
						"WaterBodyID",
						"Id",
						"osm_id;aeroway", 
						"ElecWireID",
						"Name; SubSt_ID",
						"SQFT; FEATURE; BldgID",
						"Bus_Route; Rou_Name",
						"TYPE; LOCATION; DamR_ID",
						"FEATURE; SQFT; Label_Name; EdBldg_ID",
						"Id; Location",
						"ED_No; SQFT;Label_Name",
						"OBJECTID; Comment",
						"Police_ID; SQFT; FEATURE; Label_Name",
						"LOCATION; PumpID",
						"FEATURE; SQFT; Label_Name; RelCen_ID",
						"osm_id; amenity; name",
						"LOCATOIN; FROM_;TO_;PIPE_ID; PIPE_ID",
						"LOCATION; CAPACITY; TANK_ID",
						"NAME; LOCATION; CAPASITY; Treat_ID",
						"WELL_ID",
						"OBJECTID; land_use",
						"ID; CAPTION",
						"ID; Name",
						"ID; CAPTION",
						"ID; CAPTION",
						"id; Place",
						"Name; Clinic_ID",
						"Id; Theme; Site",
						"Type; Community; Emer_ID",
						"Id; School; Type; name",
						"SitRecID; NatName",
						"ID; TYPE_2010; TYPE",
						"OBJECTID; ROAD_TYPE_; STREETNAME",
						"SQFT; FEATURE; Label_Name; Med_ID",
						"osm_id; office; building"]

############################################################################
#
# Obtain the impact information using the Tabulate intersection
############################################################################

############################################################################
# Loop through each impact layer and create the intersection table
#############################################################################
for Table in xrange(len(ImpactLayers)):
# Get the cross tabulation values and output the results as a table
	InZoneFeatures = "Antigua_FINAL_InundationClass_NEWDTM_PolygonV2"
	OuputTable = "Antigua_InundationTable_" + ImpactLayers[Table]

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
# Successfully run in ArcMap 27/03/2020 (had to set the default geodatabase!) 
# 
################################################################################
