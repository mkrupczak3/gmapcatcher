import gdal

class MapElevation:
    def __init__(self):
        driver = gdal.GetDriverByName('GTiff')
        filename = "/home/rafael/Downloads/ASTGTMV003_N39E046_dem.tif" #path to raster
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
        print "init complete"

    # in meters
    def getHeight(self, coord):
        col = int((coord[1] - self.xOrigin) / self.pixelWidth)
        row = int((self.yOrigin - coord[0] ) / self.pixelHeight)
        return self.data[row][col]
