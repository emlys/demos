import shapely

a = shapely.from_wkt('POINT (100 100)')
b = shapely.from_wkt('LINESTRING (100 -100, 100 100)')
shapely.prepare(a)
print(a.intersection(b))
