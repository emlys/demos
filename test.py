import shapely.geometry
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import numpy
import numpy.testing

origin = (444720, 3751320)
pixel_size = (30, -30)
srs = osr.SpatialReference()
srs.ImportFromEPSG(3116)

# Create a test vector
source_vector_path = 'vector.geojson'
vector_driver = ogr.GetDriverByName('GeoJSON')
vector = vector_driver.CreateDataSource(source_vector_path)
layer = target_vector.CreateLayer('test', srs=srs, geom_type=ogr.wkbPolygon)
layer_defn = target_layer.GetLayerDefn()
new_feature = ogr.Feature(layer_defn)
geometry = ogr.CreateGeometryFromWkb(
    # invalid geometry: bowtie shape with self-intersection at the center
    shapely.geometry.Polygon([
        (
            origin[0] + pixel_size[0] * x_offset,
            origin[1] + pixel_size[1] * y_offset
        ) for x_offset, y_offset in [(0, 0), (0, 1), (1, 0), (1, 1), (0, 0)]]
    ).wkb)
feature.SetGeometry(geometry)
layer.CreateFeature(new_feature)
layer = None
vector = None

# Create a test raster
source_raster_path = 'source.tif'
driver = gdal.GetDriverByName('GTIFF')
raster = driver.Create(source_raster_path, 1, 1, 1, gdal.GDT_Byte)
raster.SetProjection(srs.ExportToWkt())
raster.SetGeoTransform([
    origin[0], pixel_size[0], 0,
    origin[1], 0, pixel_size[1]])
raster = None

# Rasterize
raster = gdal.OpenEx(source_raster_path, gdal.GA_Update | gdal.OF_RASTER)
vector = gdal.OpenEx(source_vector_path, gdal.OF_VECTOR)
layer = vector.GetLayer(0)
gdal.RasterizeLayer(raster, [1], layer, burn_values=[1], options=['ALL_TOUCHED=FALSE'])

band = raster.GetRasterBand(1)
numpy.testing.assert_array_equal(band.ReadAsArray(), numpy.array([[1]])
