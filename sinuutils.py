import shapefile 
import pandas as pd
import numpy as np
import math

# readshapestopandas: function which reads a shapefile into the workspace and sets up the shapefile points in a dataframe by the lat and lon of the points. Then converts to metres by bodging using the earth as a sphere. the dataframe is ordered by the year the profile was drawn

def readshapestopandas(fname):
    reader = shapefile.Reader(fname) 
    shaperecords = reader.shapeRecords()

    shapesriver = [ ]  # set up dataframe
    #def y(shaperecord):
      # return shaperecord.record[0]

        #shaperecords.sort(key=y)
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
        
        vx = (df.x - df.x.shift()).fillna(0)
        vy = (df.y - df.y.shift()).fillna(0)
        df["segleng"] = np.sqrt(vx**2 + vy**2)
        df["ar"] = df["segleng"].cumsum()
        
        shapesriver.append((shapeid, df))
    
    return shapesriver

# transaxis: function that translates the axis about which data is assumed to oscillate/deviate from whatever its initial orientation was to being the x-axis of an x-y graph, ie reduces a 2D deviation from an assumed mean value to a 1D deviation about an axis represented by the assumed mean value

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

# warptodirect: function which transforms the profile of a river channel 
# into a straight line plane following the x-axis of zero whilst also transforming the 
# direct profile ie valley slope to a linear profile as well, thus straightening both 
# and making them follow a linear trend. Then sinuosity is caalculated in one plane only

def warptodirect(direct_profile, df):
    sx, sy = df.x, df.y
    ax, ay = direct_profile.x, direct_profile.y

    cwtx, cwty, cw = sx*0, sx*0, sx*0 # make same size zero arrays
    ar = direct_profile.ar
    for i in range(1, len(ar)):
        ax0, ax1 = ax[i-1], ax[i]
        ay0, ay1 = ay[i-1], ay[i]
        r0, r1 = ar[i-1], ar[i]
        tx, ty, tw = transaxis(r0, r1, ax0, ax1, ay0, ay1, sx, sy)
        cwtx, cwty = cwtx + tx*tw, cwty + ty*tw
        cw = cw + tw
        #plt.plot([r0, r1], [0, 0], color="k")
        #plt.plot(tx, tw, label='%d' %i)   # uncomment this to show the weighting plots

    straightenedx, straightenedy = cwtx/cw, cwty/cw
    df["straightenedx"], df["straightenedy"] = straightenedx, straightenedy
    
    vx = (df.straightenedx - df.straightenedx.shift()).fillna(0)
    vy = (df.straightenedx - df.straightenedx.shift()).fillna(0)
    df["straightenedsegleng"] = np.sqrt(vx**2 + vy**2)
    return straightenedx, straightenedy, cwtx, cwty, r0,r1

# makeweightseries: function that creates a tapered window which we can move along the channel length.

def makeweightseries(df, centreweightindex, centreweightlength):
    indexcolumn = df.index.to_series()
    w = np.exp(-((indexcolumn - centreweightindex)/centreweightlength)**2)
    return w
    
# windowed_sinuosity: function that calculates sinuosity of a channel over a window of given width with a taper as defined by the makeweightseries function
def windowed_sinuosity(df):
    
    # make unit lengths
    unitx = (df.straightenedx - df.straightenedx.shift()).fillna(0)                   
    wxs = [ ]
    wsin = [ ]
    centreweightlength = 50 # change as appropriate
    for centreweightindex in range(len(df.straightenedx)):
        w = makeweightseries(df.straightenedx, centreweightindex, centreweightlength)
        wx = sum(w*df.straightenedx)/sum(w)
        weightedstreamlength = sum(df.straightenedsegleng*w)/sum(w)
        weighteddirectlength = sum(unitx*w)/sum(w)
        weightedsinuosity = weightedstreamlength/weighteddirectlength
        wsin.append(weightedsinuosity)
        wxs.append(wx)

    wxs = np.array(wxs)
    awsin = np.array(wsin)
    df['windowedsin'] = awsin
    return wxs, awsin
    

