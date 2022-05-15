import shapefile
SHAPE_FILE_PATH = r'E:\_MIT_First_Year_Semester_1\Cluster_and_Cloud_Computing\Assignment-2\aurin_data\shp_files\spatialise-median-house-price\shp\apm_sa4_2016_timeseries-.shp'
#r'C:\Users\thoma\Desktop\IT\CCC\A2\Assignment-2\aurin_data\shp_files\spatialise-median-house-price\shp\apm_sa4_2016_timeseries-.shp'
SHAPE_FILE_PATH = './aurin_data/shp_files/spatialise-SA4\shp/apm_sa4_2016_timeseries-.shp'
shp = shapefile.Reader(SHAPE_FILE_PATH)  # open the shapefile
all_shapes = shp.shapes()  # get all the polygons
all_records = shp.records()
print(all_records)