# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.addMarker
# Widget allows adding marker on the fly from right click menu

import pygtk
import gobject
pygtk.require('2.0')
import gtk
from gmapcatcher.mapMark import MyMarkers
import numpy as np
import pyproj


from gmapcatcher.mapConst import *

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class AddMarker(gtk.Window):
    # pointer is just passing values to handler
    def __init__(self, handler, pointer):
        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")
        self.changer = True # if False then the changer is _wgs84_changed, otherwise changer is _sk42_changed
        self.useInputCordinates = False

        def _wgs84_activated(garbage, garbage_):
            self.changer = True

        def _sk42_activated(garbage, garbage_):
            self.changer = False

        def _wg84_changed(garbage):
            if self.changer == True:
                convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(self._wgs84_Lon.get_text()), np.float64(self._wgs84_Lat.get_text()))
                self._sk42_Lat.set_text(str("%.9g" % convertedLat))
                self._sk42_Lon.set_text(str("%.9g" % convertedLon))

        def _sk42_changed(garbage):
            if self.changer == False:
                convertedLon, convertedLat = pyproj.transform(self.proj_sk42, self.proj_wgs84 , np.float64(self._sk42_Lon.get_text()), np.float64(self._sk42_Lat.get_text()))
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

        def _sk42():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Latitude:"))
            self._sk42_Lat = myEntry("%.6g" % 0, 10, False)
            hbox.pack_start(self._sk42_Lat, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Longitude:"))
            self._sk42_Lon = myEntry("%.6g" % 0, 10, False)
            hbox.pack_start(self._sk42_Lon, False)
            vbox.pack_start(hbox)

            self._sk42_Lon.connect("changed", _sk42_changed)
            self._sk42_Lat.connect("changed", _sk42_changed)

            self._sk42_Lon.connect("focus_in_event", _sk42_activated)
            self._sk42_Lat.connect("focus_in_event", _sk42_activated)

            # update sk42 just to get right values, otherwise it will be 0
            _wg84_changed(None)
            return myFrame(" Sk42", vbox)

        def _markerName():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Choose Name:"))
            self._marker_name = gtk.Entry()
            self._marker_name.set_text("")
            hbox.pack_start(self._marker_name, False)
            vbox.pack_start(hbox)

            return myFrame(" Marker Name", vbox)

        def _color_debug():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Color:"))

            self.store = gtk.ListStore(gtk.gdk.Pixbuf,gobject.TYPE_STRING)

            options = [["red", "marker_combo_red.png"],
                    ["blue", "marker_combo_blue.png"],
                    ["yellow", "marker_combo_yellow.png"],
                    ["green", "marker_combo_green.png"]]

            self._marker_color = gtk.ComboBox(self.store)            

            self._marker_color.set_active(1)
            cell = gtk.CellRendererText()
            self._marker_color.pack_start(cell, True)
            self._marker_color.add_attribute(cell, 'text', 1)
        
            cell = gtk.CellRendererPixbuf()
            self._marker_color.pack_start(cell, True)
            self._marker_color.add_attribute(cell, 'pixbuf', 0)

            markers = MyMarkers() 
            for color, img in options:
                iter = self.store.append()
                pixbuf = markers.get_marker_pixbuf(15, img)
                self.store.set(iter, 0, pixbuf, 1, color)
            
            self._marker_color.set_active(1)
            hbox.pack_start(self._marker_color, False)
            vbox.pack_start(hbox)

            return myFrame(" Color", vbox)

        def use_input_cordinate_checkbox():
            hbox = gtk.HBox(False, 10)
            checkBox = gtk.CheckButton() 
            hbox.pack_start(checkBox)
            checkBox.connect("toggled", use_input_cordinate_checkbox_changed) 
            checkBox.set_label("From Input ?")
            return hbox

        def use_input_cordinate_checkbox_changed(garbage):
            if self.useInputCordinates:
                self.useInputCordinates = False
            else:
                self.useInputCordinates = True

        def btn_ok():
            button = gtk.Button(stock=gtk.STOCK_OK)
            button.connect("clicked", btn_ok_cb)
            hbox = gtk.HButtonBox()
            hbox.pack_start(button)
            hbox.set_layout(gtk.BUTTONBOX_SPREAD)
            return hbox
        
        def btn_ok_cb(button):
            color = self._marker_color.get_active()
            if self.useInputCordinates == True:
                handler(color,
                            str(self._marker_name.get_text()),
                            pointer,
                            (float(self._wgs84_Lat.get_text()), float(self._wgs84_Lon.get_text()), 1))
            else:
                handler(color,
                            str(self._marker_name.get_text()),
                            pointer)
            self.destroy()

        gtk.Window.__init__(self)

        hbox = gtk.HBox(False, 20)
        vbox = gtk.VBox(False, 5)
        vbox.pack_start(_color_debug())
        vbox.pack_start(_markerName())
        vbox.pack_start(_wgs84())
        vbox.pack_start(_sk42())
        vbox.pack_start(use_input_cordinate_checkbox())
        hbox.pack_start(btn_ok())
        vbox.pack_start(hbox)

        self.add(vbox)
        self.set_title("Add New Marker")
        self.set_border_width(10)
        self.show_all()
