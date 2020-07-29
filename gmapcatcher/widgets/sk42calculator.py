# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.sk42calculator
# Widget that allows calculating wgs to sk42 on the fly

import pygtk
pygtk.require('2.0')
import gtk
import numpy as np
from WGS84_SK42_Translator import Translator as converter
import pyproj

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class Sk42Calculator(gtk.Window):
    def __init__(self):
        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")
        # lon, lat = pyproj.transform(pyproj.Proj(self.proj_wgs84, self.proj_sk42 , Lon, Lat)

        self.changer = [False, False, False] # if False then the changer is _wgs84_changed, otherwise changer is _sk42_changed
        self.useInputCordinates = False

        def _wgs84_activated(garbage, garbage_):
            self.changer = [1,0,0]

        # def _sk42_activated(garbage, garbage_):
        #     self.changer = [0,1,0]

        def _sk42_full_activated(garbage, garbage_):
            self.changer = [0,0,1]

        def _wg84_changed(garbage):
            if self.changer == [1,0,0]:
                print self._wgs84_Lon.get_text()
                convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(self._wgs84_Lon.get_text()), np.float64(self._wgs84_Lat.get_text()))
                self._sk42_Lat_full.set_text(str("%.9g" % convertedLat))
                self._sk42_Lon_full.set_text(str("%.9g" % convertedLon))

        def _sk42_full_changed(garbage):
            if self.changer == [0,0,1]:
                convertedLon, convertedLat = pyproj.transform(self.proj_sk42, self.proj_wgs84 , np.float64(self._sk42_Lon_full.get_text()), np.float64(self._sk42_Lat_full.get_text()))
                self._wgs84_Lat.set_text(str("%.9g" % convertedLat))
                self._wgs84_Lon.set_text(str("%.9g" % convertedLon))

        def _wgs84():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Latitude:"))
            self._wgs84_Lat = myEntry("%.9g" % 39.930474, 10, False)
            hbox.pack_start(self._wgs84_Lat, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Longitude:"))
            self._wgs84_Lon = myEntry("%.9g" % 46.84519, 10, False)
            hbox.pack_start(self._wgs84_Lon, False)
            vbox.pack_start(hbox)

            self._wgs84_Lon.connect("changed", _wg84_changed)
            self._wgs84_Lat.connect("changed", _wg84_changed)

            self._wgs84_Lon.connect("focus_in_event", _wgs84_activated)
            self._wgs84_Lat.connect("focus_in_event", _wgs84_activated)
            return myFrame(" Wgs84", vbox)


        def _sk42_full():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("X:"))
            self._sk42_Lat_full = myEntry("%.6g" % 0, 10, False)
            hbox.pack_start(self._sk42_Lat_full, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Y:"))
            self._sk42_Lon_full = myEntry("%.6g" % 0, 10, False)
            hbox.pack_start(self._sk42_Lon_full, False)
            vbox.pack_start(hbox)

            self._sk42_Lon_full.connect("changed", _sk42_full_changed)
            self._sk42_Lat_full.connect("changed", _sk42_full_changed)

            self._sk42_Lon_full.connect("focus_in_event", _sk42_full_activated)
            self._sk42_Lat_full.connect("focus_in_event", _sk42_full_activated)

            return myFrame("SK42 full EPSG:28468", vbox)

        # def btn_calculate():
        #     button = gtk.Button(stock=gtk.STOCK_OK)
        #     button.connect("clicked", btn_calculate_cb)
        #     hbox = gtk.HButtonBox()
        #     hbox.pack_start(button)
        #     hbox.set_layout(gtk.BUTTONBOX_SPREAD)
        #     return hbox
        #
        # def btn_calculate_cb(button):
        #     height = 900 
        #     convertedLat, convertedLon = self.transformer_wgs_sk42.transform(np.float64(self._wgs84_Lat.get_text()), np.float64(self._wgs84_Lon.get_text()))
        #
        #     self._sk42_lat.set_text(str("%.9g" % convertedLat)[2:7])
        #     self._sk42_lon.set_text(str("%.9g" % convertedLon)[1:6])

        gtk.Window.__init__(self)

        hbox = gtk.HBox(False, 20)
        vbox = gtk.VBox(False, 5)
        # hbox.pack_start(btn_calculate())
        vbox.pack_start(hbox)
        vbox.pack_start(_wgs84())
        vbox.pack_start(_sk42_full())

        self.add(vbox)
        self.set_title("Sk42 Calculator")
        self.set_border_width(10)
        self.show_all()

        # update sk42 just to get right values, otherwise it will be 0
        _wg84_changed(None)
