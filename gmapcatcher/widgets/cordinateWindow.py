# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that displays azimuth, lat/long, sk42 cordinates

import pygtk
pygtk.require('2.0')
import gtk
import numpy as np
from WGS84_SK42_Translator import Translator as converter
from pyproj import Transformer

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class CordinateWindow(gtk.Window):
    def __init__(self, azimuth, distance, start_point, end_point):
        azimuth_hbox = gtk.HBox(False, 20)
        sk42_hbox = gtk.HBox(False, 20)
        sk42_hbox_zone = gtk.HBox(False, 20)

        self.transformer_wgs_sk42 = Transformer.from_crs("EPSG:4284", "EPSG:28468")
        self.transformer_sk42_wgs = Transformer.from_crs("EPSG:28468", "EPSG:4284")

        def _area():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("azimuth:"))
            self.entry = myEntry("%.6g" % azimuth, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("distance:"))
            self.entry = myEntry("%.6g" % distance, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame(" Calculated Azimuth and Distance", vbox)

        def _start_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.azimuth = myEntry("%.6f" % start_point[0], 10, False)
            hbox.pack_start(self.azimuth, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.distance = myEntry("%.6f" % start_point[1], 10, False)
            hbox.pack_start(self.distance, False)
            vbox.pack_start(hbox)

            return myFrame("Start Point", vbox)

        def _end_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.entry = myEntry("%.6f" % end_point[0], 10, False)
            print(end_point[0])
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.entry = myEntry("%.6f" % end_point[1], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("End Point", vbox)

        def _wgs_to_sk42_start_point():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(np.float64(start_point[0]),np.float64(start_point[1]),height)
            # convertedLon = converter.WGS84_SK42_Long(np.float64(start_point[0]),np.float64(start_point[1]),height)
            convertedLat, convertedLon = self.transformer_wgs_sk42.transform(np.float64(start_point[0]), np.float64(start_point[1]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.entry = myEntry(str("%.9f" % convertedLat)[2:7], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.entry = myEntry(str("%.9f" % convertedLon)[1:6], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 start point EPSG:28468 XY", vbox)

        def _wgs_to_sk42_end_point_zone():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(end_point[0],end_point[1],height)
            # convertedLon = converter.WGS84_SK42_Long(end_point[0],end_point[1],height)
            convertedLat, convertedLon = self.transformer_wgs_sk42.transform(np.float64(end_point[0]), np.float64(end_point[1]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.entry = myEntry(str("%.9f" % convertedLat), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.entry = myEntry(str("%.9f" % convertedLon), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 full EPSG:28468", vbox)

        def _wgs_to_sk42_start_point_zone():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(np.float64(start_point[0]),np.float64(start_point[1]),height)
            # convertedLon = converter.WGS84_SK42_Long(np.float64(start_point[0]),np.float64(start_point[1]),height)
            convertedLat, convertedLon = self.transformer_wgs_sk42.transform(np.float64(start_point[0]), np.float64(start_point[1]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.entry = myEntry(str("%.9f" % convertedLat), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.entry = myEntry(str("%.9f" % convertedLon), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 full EPSG:28468", vbox)

        def _wgs_to_sk42_end_point():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(end_point[0],end_point[1],height)
            # convertedLon = converter.WGS84_SK42_Long(end_point[0],end_point[1],height)
            convertedLat, convertedLon = self.transformer_wgs_sk42.transform(np.float64(end_point[0]), np.float64(end_point[1]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.entry = myEntry(str("%.9f" % convertedLat)[2:7], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.entry = myEntry(str("%.9f" % convertedLon)[1:6], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 end point EPSG:28468 XY", vbox)


        gtk.Window.__init__(self)
        vbox = gtk.VBox(False)
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(_area())

        azimuth_hbox.pack_start(_start_point())
        azimuth_hbox.pack_start(_end_point())

        sk42_hbox.pack_start(_wgs_to_sk42_start_point())
        sk42_hbox.pack_start(_wgs_to_sk42_end_point())

        sk42_hbox_zone.pack_start(_wgs_to_sk42_start_point_zone())
        sk42_hbox_zone.pack_start(_wgs_to_sk42_end_point_zone())

        vbox.pack_start(hbox)
        vbox.pack_start(azimuth_hbox)
        vbox.pack_start(sk42_hbox)
        vbox.pack_start(sk42_hbox_zone)
        self.add(vbox)
        self.set_title("Azimuth and Distance Calculator")
        self.set_border_width(10)
        self.show_all()
