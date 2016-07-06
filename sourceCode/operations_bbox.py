__author__ = 'cesar17'
from geolocation_bbox import GeoLocation

def is_in_bounding_box(location, bbox):
    longitud= location[0]
    latitud = location[1]
    minLong = bbox[0]
    minLat = bbox[1]
    maxLong = bbox[2]
    maxLat = bbox[3]
    return longitud >= minLong and longitud <= maxLong and latitud >= minLat and latitud <= maxLat

def get_index_bbox(location, bboxes):
    for key in bboxes.iterkeys():
        bbox = bboxes[key]
        if is_in_bounding_box(location, bbox):
            # print key
            return key
        else:
            return '-'

def set_bbox_top_cosas_hacer():
    # a Iglesia de la compania de jesus
    # b Teleferico de quito

    sitios = {'a':[-78.51385, -0.221065], 'b':[-78.53728, -0.186694]}
    bboxes = {}
    for key in sitios.iterkeys():
        value = sitios[key]
        longitude = value[0]
        latitude = value[1]
        loc = GeoLocation.from_degrees(latitude, longitude)
        distance = 1  # 1 kilometer
        SW_loc, NE_loc = loc.bounding_locations(distance)
        minlong = SW_loc.deg_lon
        minlat = SW_loc.deg_lat
        maxlong = NE_loc.deg_lon
        maxlat = NE_loc.deg_lat
        bboxes[key] = [minlong, minlat, maxlong, maxlat]

    aux = get_index_bbox([-79.8833,-2.1833], bboxes)
    print aux

set_bbox_top_cosas_hacer()