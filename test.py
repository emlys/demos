import shapely.geometry
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

default_origin = (444720, 3751320)
default_pixel_size = (30, -30)
default_epsg = 3116
default_srs = osr.SpatialReference()
default_srs.ImportFromEPSG(default_epsg)

coordinates = []
for pixel_x_offset, pixel_y_offset in [
        (0, 0), (0, 1), (1, 0), (1, 1), (0, 0)]:
    coordinates.append((
        default_origin[0] + default_pixel_size[0] * pixel_x_offset,
        default_origin[1] + default_pixel_size[1] * pixel_y_offset
    ))
source_vector_path = 'vector.geojson'
source_raster_path = 'source.tif'

shapely_feature = shapely.geometry.Polygon(coordinates)
vector_driver = ogr.GetDriverByName('GeoJSON')
target_vector = vector_driver.CreateDataSource(source_vector_path)
layer_name = 'test'
target_layer = target_vector.CreateLayer(
    layer_name, srs=default_srs, geom_type=ogr.wkbPolygon)
layer_defn = target_layer.GetLayerDefn()
new_feature = ogr.Feature(layer_defn)
new_geometry = ogr.CreateGeometryFromWkb(shapely_feature.wkb)
new_feature.SetGeometry(new_geometry)
target_layer.CreateFeature(new_feature)
target_layer = None
target_vector = None

driver = gdal.GetDriverByName('GTIFF')
raster = driver.Create(
    source_raster_path, 1, 1, 1,
    gdal.GDT_Byte)
raster.SetProjection(default_srs.ExportToWkt())
raster.SetGeoTransform([
    default_origin[0], default_pixel_size[0], 0,
    default_origin[1], 0, default_pixel_size[1]])
raster = None

raster = gdal.OpenEx(source_raster_path, gdal.GA_Update | gdal.OF_RASTER)
vector = gdal.OpenEx(source_vector_path, gdal.OF_VECTOR)
layer = vector.GetLayer(0)

gdal.RasterizeLayer(
    raster, [1], layer, burn_values=[1],
    options=['ALL_TOUCHED=FALSE'])

band = raster.GetRasterBand(1)
assert band.ReadAsArray()[0][0] == 1


