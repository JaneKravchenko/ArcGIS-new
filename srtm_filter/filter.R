library(raster)
library(tiff) 
library(rgdal)


str_name<-'/home/alex/Jane/ArcGIS-new/images/clipped_all_map.tif'
srtm = raster(str_name)
srtm_too<- focal(srtm, w=matrix(1/49,nc=7,nr=7))

rf <- writeRaster(srtm_too, filename="name.tif", format="GTiff", overwrite=TRUE)

hist(srtm)
hist(srtm_too)
