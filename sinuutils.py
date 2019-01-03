import shapefile 
import pandas as pd
import math

# readshapestopandas: function which reads a shapefile into the workspace and sets up the shapefile points in a dataframe by the lat and lon of the points. Then converts to metres by bodging using the earth as a sphere

def readshapestopandas(fname):
    reader = shapefile.Reader(fname) 
    shaperecords = reader.shapeRecords()

    shapesriver = [ ]  # set up dataframe
    for shaperecord in shaperecords:
        pshp = shaperecord.shape.points
        shapeid = shaperecord.record[0] # the shapes are identified by the first attribute field
        # this is either the channel id or the year the channel was drawn
        lngs, lats = list(zip(*pshp))
        df = pd.DataFrame({"lat":lats, "lng":lngs}) # dataframe equivalent of matrix/array in matlab
        lat0, lng0 = df.lat.iloc[0], df.lng.iloc[0]

        earthrad = 6378137
        nyfac = 2*math.pi*earthrad/360
        exfac = nyfac*math.cos(math.radians(lat0))
        df["x"] = (df.lng - lng0)*exfac # x positions of channel in dataframe
        df["y"] = (df.lat - lat0)*nyfac # y positions of channel in dataframe
        
        df.x**2
        
        shapesriver.append((shapeid, df))
    
    return shapesriver

# transaxis: function which transforms the profile of a river channel into a straight line plane following the x-axis

def transaxis(r0, r1, ax0, ax1, ay0, ay1, sx, sy):
    axv, ayv = ax1 - ax0, ay1 - ay0
    alen = math.hypot(axv, ayv)
    osx, osy = sx - ax0, sy - ay0
    osdotav = (osx*axv + osy*ayv)/alen
    osdotperpav = (osx*ayv - osy*axv)/alen
    tx = osdotav + r0
    ty = osdotperpav
    tw = 1.0/(0.6 + abs(osdotav/alen - 0.5).clip_lower(0.4))**2   # weighting
    return tx, ty, tw
