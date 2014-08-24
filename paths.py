import pandas as pd
import numpy as np
from gcmap import GCMapper, Gradient
from PIL import Image, ImageFilter

ROUTE_COLS = ('airline_name', 'airline_id', 'source_code', 'source_id', 'dest_code', 'dest_id', 'codeshare', 'stops', 'equiptment')
AIRPORT_COLS = ('airport_id', 'airport_name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone', 'dst')

routes = pd.read_csv('routes.dat', header=None, names=ROUTE_COLS, na_values=['\\N'])
airports = pd.read_csv('airports.dat', header=None, names=AIRPORT_COLS)

airport_pairs = routes.groupby(('source_id', 'dest_id')).size()
airport_pairs = airport_pairs.reset_index()
airport_pairs.columns = ('source_id', 'dest_id', 'cnt')

airport_pairs = airport_pairs.merge(airports, left_on='source_id', right_on='airport_id') \
                             .merge(airports, left_on='dest_id', right_on='airport_id', suffixes=('_source', '_dest'))
                             

g = Gradient([(   0,   204,   255,   131),
              ( 0.4,    51,   255,    51),
              (   1,     0,     0,     0)])


gcm = GCMapper(cols=g, bgcol=(255,255,255))
gcm.set_data(airport_pairs.longitude_source, airport_pairs.latitude_source, airport_pairs.longitude_dest, airport_pairs.latitude_dest, airport_pairs.cnt)
img = gcm.draw()
img.save('test.png')

original = Image.open("test.png")
original.show()