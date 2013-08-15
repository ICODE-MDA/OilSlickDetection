"""
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
The input image, ENVISTA ASAR image in GeoTiff format, has been calibrated. 
**ff changes if the input image is hsitogram equalised instead calibrated.
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
"""
import osgeo.gdal as gdal
from gdalconst import *
from numpy import *
import math
import epr
from scipy import array
import scipy.misc
import matplotlib.pyplot as plt
import sys
import scipy.signal


"#Opening file"
dataset = gdal.Open( "input_filename", GA_ReadOnly )
if dataset is None:
            print "The dataset could not be openned"
            sys.exit(-1)



"#Creating GeoTiff FILE"
format = "GTiff"
driver = gdal.GetDriverByName( format )
metadata = driver.GetMetadata()


"#Fetching a raster band"
band = dataset.GetRasterBand(1)
cols = dataset.RasterXSize
rows = dataset.RasterYSize
counts = dataset.RasterCount

data = band.ReadAsArray( 0, 0, cols, rows)

ice = data

print 'starting filtering'

z = scipy.signal.medfilt2d(ice, kernel_size=11)

print 'Filtering done'

ysize, xsize = z.shape

output_data = zeros((ysize,xsize), uint8)


"declaring window size"
wy,wx = 5000,5000


print 'now on loop'


'#Detection method'
for x in xrange(0,ysize,wx):
    for y in xrange(0,xsize,wy):
        b = z[x:x+wy, y:y+wy]
        f = std(b)/mean(b)	
        c = std(b)
        ff = 0.00031
        threshold = (float(f) / c) * ff  
        b[b > threshold] = 255
        b[b < threshold] = 0
        output_data[x:x+wy, y:y+wx] = b

print 'loop done'


if metadata.has_key(gdal.DCAP_CREATE) \
   and metadata[gdal.DCAP_CREATE] == 'YES':
    print 'Driver %s supports Create() method.' % format



out_data = driver.Create( 'output_file_name', xsize, ysize, 1, gdal.GDT_Byte )
out_data.GetRasterBand(1).WriteArray(output_data)
out_data = None
dataset = None


