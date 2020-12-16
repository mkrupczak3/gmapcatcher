import gdal
from gmapcatcher.mapConst import *
import os

class MapElevation:
    def __init__(self):
        try:
            driver = gdal.GetDriverByName('GTiff')
            localPath = os.path.expanduser(DEFAULT_PATH)
            filename = os.path.join(localPath, MAP_ELEVATION_TIFF) #path to raster
            dataset = gdal.Open(filename)
            band = dataset.GetRasterBand(1)

            cols = dataset.RasterXSize
            rows = dataset.RasterYSize

            transform = dataset.GetGeoTransform()

            self.xOrigin = transform[0]
            self.yOrigin = transform[3]
            self.pixelWidth = transform[1]
            self.pixelHeight = -transform[5]

            self.data = band.ReadAsArray(0, 0, cols, rows)
        except Exception as ex:
            print ex

    # in meters
    def getHeight(self, coord):
        try:
            col = int((coord[1] - self.xOrigin) / self.pixelWidth)
            row = int((self.yOrigin - coord[0] ) / self.pixelHeight)
            return self.data[row][col]
        except Exception as ex:
            print coord
            print ex
