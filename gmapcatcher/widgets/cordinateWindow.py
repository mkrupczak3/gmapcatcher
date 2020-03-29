# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that allows Export of entire locations to new tiles repository

import pygtk
pygtk.require('2.0')
import gtk

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class CordinateWindow(gtk.Window):
    def __init__(self, azimuth, distance):
        azimuth_hbox = gtk.HBox(False, 20)
        self._azimuth = azimuth
        self._distance = distance
        def _area(azimuth, distance):
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("azimuth:"))
            self.azimuth = myEntry("%.6g" % azimuth, 10, False)
            hbox.pack_start(self.azimuth, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("distance:"))
            self.distance = myEntry("%.6g" % distance, 10, False)
            hbox.pack_start(self.distance, False)
            vbox.pack_start(hbox)

            return myFrame(" Calculated Azimuth and Distance", vbox)

        gtk.Window.__init__(self)
        vbox = gtk.VBox(False)
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(_area(self._azimuth, self._distance))
        vbox.pack_start(hbox)
        self.add(vbox)
        self.set_title("Azimuth and Distance Calculator")
        self.set_border_width(10)
        self.show_all()
