# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that allows Export of entire locations to new tiles repository

import pygtk
pygtk.require('2.0')
import gtk
import numpy as np
from WGS84_SK42_Translator import Translator as converter
from pyproj import CRS, Transformer

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class Sk42Calculator(gtk.Window):
    _wgs84_lat = None
    _wgs84_Lon = None
    _sk42_lat = None
    _sk42_lon = None
    def __init__(self):
        self.transformer_wgs_sk42 = Transformer.from_crs("EPSG:4284", "EPSG:28468")
        # self.transformer_sk42_wgs = Transformer.from_crs("EPSG:28468", "EPSG:4284")
        def _wgs84():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Latitude:"))
            self.entry = myEntry("%.9g" % 39.830474, 10, False)
            self._wgs84_Lat = self.entry
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Longitude:"))
            self.entry = myEntry("%.9g" % 46.74519, 10, False)
            self._wgs84_Lon = self.entry
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)
            return myFrame(" Wgs84", vbox)

        def _sk42():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Latitude:"))
            self.entry = myEntry("%.6g" % 0, 10, False)
            self._sk42_lat = self.entry
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Longitude:"))
            self.entry = myEntry("%.6g" % 0, 10, False)
            self._sk42_lon = self.entry
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)
            return myFrame(" Sk42", vbox)

        def btn_calculate():
            button = gtk.Button(stock=gtk.STOCK_OK)
            button.connect("clicked", btn_calculate_clicked)
            hbox = gtk.HButtonBox()
            hbox.pack_start(button)
            hbox.set_layout(gtk.BUTTONBOX_SPREAD)
            return hbox

        def btn_calculate_clicked(button):
            height = 900 
            convertedLat, convertedLon = self.transformer_wgs_sk42.transform(np.float64(self._wgs84_Lat.get_text()), np.float64(self._wgs84_Lon.get_text()))

            self._sk42_lat.set_text(str("%.9g" % convertedLat)[2:7])
            self._sk42_lon.set_text(str("%.9g" % convertedLon)[1:6])

        gtk.Window.__init__(self)
        hbox = gtk.HBox(False, 20)
        vbox = gtk.VBox(False, 5)
        hbox.pack_start(btn_calculate())
        vbox.pack_start(hbox)
        vbox.pack_start(_wgs84())
        vbox.pack_start(_sk42())
        self.add(vbox)
        self.set_title("Sk42 Calculator")
        self.set_border_width(10)
        self.show_all()
