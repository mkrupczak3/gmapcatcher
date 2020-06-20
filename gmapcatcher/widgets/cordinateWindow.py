# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that allows Export of entire locations to new tiles repository

import pygtk
pygtk.require('2.0')
import gtk
from WGS84_SK42_Translator import Translator as converter

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class CordinateWindow(gtk.Window):
    def __init__(self, azimuth, distance, start_point, end_point):
        azimuth_hbox = gtk.HBox(False, 20)
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
            hbox.pack_start(lbl("longitude:"))
            self.azimuth = myEntry("%.6f" % start_point[0], 10, False)
            hbox.pack_start(self.azimuth, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.distance = myEntry("%.6f" % start_point[1], 10, False)
            hbox.pack_start(self.distance, False)
            vbox.pack_start(hbox)

            return myFrame("Start Point", vbox)

        def _end_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.entry = myEntry("%.6f" % end_point[0], 10, False)
            print(end_point[0])
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.entry = myEntry("%.6f" % end_point[1], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("End Point", vbox)

        def _wgs_to_sk42():
            height = 0 
            convertedLat = converter.WGS84_SK42_Lat(end_point[1],end_point[0],height)
            convertedLong = converter.WGS84_SK42_Long(end_point[1],end_point[0],height)

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("longitude:"))
            self.entry = myEntry("%.9f" % convertedLong, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("latitude:"))
            self.entry = myEntry("%.9f" % convertedLat, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42", vbox)


        gtk.Window.__init__(self)
        vbox = gtk.VBox(False)
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(_area())
        hbox.pack_start(_start_point())
        hbox.pack_start(_end_point())
        hbox.pack_start(_wgs_to_sk42())
        vbox.pack_start(hbox)
        self.add(vbox)
        self.set_title("Azimuth and Distance Calculator")
        self.set_border_width(10)
        self.show_all()
