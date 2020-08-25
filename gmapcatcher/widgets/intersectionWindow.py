# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that displays azimuth, lat/long, sk42 cordinates

import pygtk
import gobject
pygtk.require('2.0')
import gtk
import numpy as np
from WGS84_SK42_Translator import Translator as converter
import pyproj
from gmapcatcher.mapUtils import computeIntersection
from gmapcatcher.mapMark import MyMarkers
from gmapcatcher.mapConst import *

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class IntersectionWindow(gtk.Window):
    # in this case pointer is useless, supporting old code
    # pointer is just passing values to handler
    def __init__(self, first_point, second_point, handler, pointer):
        if first_point[0] == second_point[0]:
            md = gtk.MessageDialog(self, 
                    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
                    gtk.BUTTONS_CLOSE, "пожалуйста, выберите разные точки")
            md.run()
            md.destroy()
            return

        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")
        sk42_hbox_full = gtk.HBox(False, 20)
        azimuth_hbox = gtk.HBox(False, 20)
        angles = gtk.HBox(False, 20)

        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")

        def _first_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.entry = myEntry("%.6f" % first_point[0], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.distance = myEntry("%.6f" % first_point[1], 10, False)
            hbox.pack_start(self.distance, False)
            vbox.pack_start(hbox)

            return myFrame("базовая точка", vbox)

        def _second_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.entry = myEntry("%.6f" % second_point[0], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.entry = myEntry("%.6f" % second_point[1], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("цель", vbox)

        def _wgs_to_sk42():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(second_point[0],second_point[1],height)
            # convertedLon = converter.WGS84_SK42_Long(second_point[0],second_point[1],height)
            convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(second_point[1]), np.float64(second_point[0]))

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

            return myFrame("цель ск-42 EPSG:28468", vbox)

        def _wgs_to_sk42_start_full():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(np.float64(first_point[0]),np.float64(first_point[1]),height)
            # convertedLon = converter.WGS84_SK42_Long(np.float64(first_point[0]),np.float64(first_point[1]),height)
            convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(first_point[1]), np.float64(first_point[0]))

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

            return myFrame("базовая точка ск-42 EPSG:28468", vbox)

        def _angle1():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("angle:"))
            self.angle1 = myEntry("%.9g" % 0, 10, False)
            hbox.pack_start(self.angle1, False)
            vbox.pack_start(hbox)

            return myFrame(" angle 1", vbox)

        def _angle2():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("angle:"))
            self.angle2 = myEntry("%.9g" % 0, 10, False)
            hbox.pack_start(self.angle2, False)
            vbox.pack_start(hbox)

            return myFrame(" angle 2", vbox)

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
                    ["green", "marker_combo_green.png"],
                    ["camera_purple", "camera_combo_purple.png"]]

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

        def btn_ok():
            button = gtk.Button(stock=gtk.STOCK_OK)
            button.connect("clicked", btn_ok_cb)
            hbox = gtk.HButtonBox()
            hbox.pack_start(button)
            hbox.set_layout(gtk.BUTTONBOX_SPREAD)
            return hbox

        def btn_ok_cb(button):
            if float(self.angle1.get_text()) == float(self.angle2.get_text()):
                md = gtk.MessageDialog(self, 
                        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
                        gtk.BUTTONS_CLOSE, "линии не пересекаются\nпожалуйста, напишите разные углы !!!")
                md.run()
                md.destroy()
            elif abs(float(self.angle1.get_text()) - float(self.angle2.get_text())) == 180:
                md = gtk.MessageDialog(self, 
                        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
                        gtk.BUTTONS_CLOSE, "линии не пересекаются\nпожалуйста, напишите непоралелные углы !!!")
                md.run()
                md.destroy()
            else:
                color = self._marker_color.get_active()
                intersectedLat, interesctedLon = computeIntersection(first_point[0], first_point[1], float(self.angle1.get_text()), second_point[0], second_point[1], float(self.angle2.get_text()))
                handler(color,
                            str(self._marker_name.get_text()),
                            pointer,
                            (intersectedLat, interesctedLon, 1))
                self.destroy()

        gtk.Window.__init__(self)
        vbox = gtk.VBox(False)
        hbox = gtk.HBox(False, 10)

        azimuth_hbox.pack_start(_first_point())
        azimuth_hbox.pack_start(_second_point())
        angles.pack_start(_angle1())
        angles.pack_start(_angle2())

        sk42_hbox_full.pack_start(_wgs_to_sk42_start_full())
        sk42_hbox_full.pack_start(_wgs_to_sk42())

        vbox.pack_start(hbox)
        vbox.pack_start(sk42_hbox_full)
        vbox.pack_start(azimuth_hbox)
        vbox.pack_start(angles)
        self.add(vbox)
        vbox.pack_start(_markerName())
        vbox.pack_start(_color_debug())
        vbox.pack_start(btn_ok())
        self.set_title("Azimuth and Distance Calculator")
        self.set_border_width(10)
        self.show_all()
