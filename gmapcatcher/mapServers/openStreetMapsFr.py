## @package gmapcatcher.mapServers.openStreetMapsFr
# All the interaction with French openstreetmap.fr

from gmapcatcher.mapConst import MAP_MAX_ZOOM_LEVEL


## Returns a template URL for the openStreetMaps
def layer_url_template():
    return 'http://%s.tile.openstreetmap.fr/osmfr/%i/%i/%i.png'

## Returns the URL to the openStreetMaps tile
def get_url(counter, coord, layer, conf):
    server = ['a', 'b', 'c']
    return layer_url_template() % (server[counter % 3],
                MAP_MAX_ZOOM_LEVEL - coord[2], coord[0], coord[1])
