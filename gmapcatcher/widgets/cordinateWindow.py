# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that displays azimuth, lat/long, sk42 cordinates

import pygtk
pygtk.require('2.0')
import gtk
import numpy as np
from WGS84_SK42_Translator import Translator as converter
import pyproj

import math
import matplotlib.pyplot as plt
from gmapcatcher.mapElevation import MapElevation

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class CordinateWindow(gtk.Window):
    def __init__(self, azimuth, distance, start_point, end_point, compass_encoder_diff, mag_merid, true_north, show_elevation = False):
        if start_point[0] == end_point[0]:
            md = gtk.MessageDialog(self, 
                    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
                    gtk.BUTTONS_CLOSE, "пожалуйста, выберите разные точки")
            md.run()
            md.destroy()
            return
        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")
        azimuth_hbox = gtk.HBox(False, 20)
        sk42_hbox_full = gtk.HBox(False, 20)

        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")

        def _area():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("азимут:"))
            self.entry = myEntry("%.6g" % azimuth, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox.pack_start(lbl("Дирекционный угол:"))
            self.entry = myEntry("%.2f" % float((azimuth - true_north)/6), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox.pack_start(lbl("маг. угол с искажением:"))
            self.entry = myEntry("%.2f" % float((azimuth + mag_merid)/6), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("azimuth input:"))
            self.entry = myEntry("%.2f" % distance, 10, False)
            hbox.pack_start(self.entry, False)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("encoder:"))
            azimuth_compass_encoder_diff = azimuth + compass_encoder_diff
            # correcting the diff hwen its above 360
            if azimuth_compass_encoder_diff >= 360:
                azimuth_compass_encoder_diff -= 360
            self.entry = myEntry("%.2f" % azimuth_compass_encoder_diff, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox.pack_start(lbl("distance:"))
            self.entry = myEntry("%.1f" % distance, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame(" Calculated Azimuth and Distance", vbox)

        def _start_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.azimuth = myEntry("%.6f" % start_point[0], 10, False)
            hbox.pack_start(self.azimuth, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.distance = myEntry("%.6f" % start_point[1], 10, False)
            hbox.pack_start(self.distance, False)
            vbox.pack_start(hbox)

            return myFrame("базовая точка", vbox)

        def _end_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.entry = myEntry("%.6f" % end_point[0], 10, False)
            print(end_point[0])
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.entry = myEntry("%.6f" % end_point[1], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("цель", vbox)

        def _wgs_to_sk42_end_full():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(end_point[0],end_point[1],height)
            # convertedLon = converter.WGS84_SK42_Long(end_point[0],end_point[1],height)
            convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(end_point[1]), np.float64(end_point[0]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("X:"))
            self.entry = myEntry(str("%.0f" % convertedLat), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Y:"))
            self.entry = myEntry(str("%.0f" % convertedLon), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 full EPSG:28468", vbox)

        def _wgs_to_sk42_start_full():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(np.float64(start_point[0]),np.float64(start_point[1]),height)
            # convertedLon = converter.WGS84_SK42_Long(np.float64(start_point[0]),np.float64(start_point[1]),height)
            convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(start_point[1]), np.float64(start_point[0]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.entry = myEntry(str("%.0f" % convertedLat), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.entry = myEntry(str("%.0f" % convertedLon), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 full EPSG:28468", vbox)

        def show_elevation_profile():
            mapElevation = MapElevation()

            #START-END POINT
            P1=start_point
            P2=end_point

            #NUMBER OF POINTS
            s=100
            interval_lat=(P2[0]-P1[0])/s #interval for latitude
            interval_lon=(P2[1]-P1[1])/s #interval for longitude

            #SET A NEW VARIABLE FOR START POINT
            lat0=P1[0]
            lon0=P1[1]

            #LATITUDE AND LONGITUDE LIST
            lat_list=[lat0]
            lon_list=[lon0]

            #GENERATING POINTS
            for i in range(s):
                lat_step=lat0+interval_lat
                lon_step=lon0+interval_lon
                lon0=lon_step
                lat0=lat_step
                lat_list.append(lat_step)
                lon_list.append(lon_step)

            #HAVERSINE FUNCTION
            def haversine(lat1,lon1,lat2,lon2):
                lat1_rad=math.radians(lat1)
                lat2_rad=math.radians(lat2)
                lon1_rad=math.radians(lon1)
                lon2_rad=math.radians(lon2)
                delta_lat=lat2_rad-lat1_rad
                delta_lon=lon2_rad-lon1_rad
                a=math.sqrt((math.sin(delta_lat/2))**2+math.cos(lat1_rad)*math.cos(lat2_rad)*(math.sin(delta_lon/2))**2)
                d=2*6371000*math.asin(a)
                return d

            #DISTANCE CALCULATION
            d_list=[]
            elev_list=[]
            for j in range(len(lat_list)):
                lat_p=lat_list[j]
                lon_p=lon_list[j]
                elev_list.append(mapElevation.getHeight((lat_p, lon_p)))
                dp=haversine(lat0,lon0,lat_p,lon_p)/1000 #km
                d_list.append(dp)
            d_list_rev=d_list[::-1] #reverse list

            #BASIC STAT INFORMATION
            mean_elev=round((sum(elev_list)/len(elev_list)),3)
            min_elev=min(elev_list)
            max_elev=max(elev_list)
            distance=d_list_rev[-1]

            #PLOT ELEVATION PROFILE
            base_reg=0
            plt.figure(figsize=(10,4))
            plt.plot(d_list_rev,elev_list)
            plt.plot([0,distance],[min_elev,min_elev],'--g',label='min: '+str(min_elev)+' m')
            plt.plot([0,distance],[max_elev,max_elev],'--r',label='max: '+str(max_elev)+' m')
            plt.plot([0,distance],[mean_elev,mean_elev],'--y',label='ave: '+str(mean_elev)+' m')
            plt.fill_between(d_list_rev,elev_list,base_reg,alpha=0.1)
            plt.text(d_list_rev[0],elev_list[0],"P1")
            plt.text(d_list_rev[-1],elev_list[-1],"P2")
            plt.xlabel("Distance(km)")
            plt.ylabel("Elevation(m)")
            plt.grid()
            plt.legend(fontsize='small')

        if show_elevation == True:
            show_elevation_profile()
            plt.show()
        else:
            gtk.Window.__init__(self)
            vbox = gtk.VBox(False)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(_area())

            azimuth_hbox.pack_start(_start_point())
            azimuth_hbox.pack_start(_end_point())

            sk42_hbox_full.pack_start(_wgs_to_sk42_start_full())
            sk42_hbox_full.pack_start(_wgs_to_sk42_end_full())

            vbox.pack_start(hbox)
            vbox.pack_start(azimuth_hbox)
            vbox.pack_start(sk42_hbox_full)
            self.add(vbox)
            self.set_title("Azimuth and Distance Calculator")
            self.set_border_width(10)
            self.show_all()
