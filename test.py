import shapely

a = shapely.from_wkt('POLYGON ((110 110, 110 100, 100 100, 100 110, 110 110))')
b = shapely.from_wkt('LINESTRING (100 -100, 100 100)')
print(a.intersection(b))
