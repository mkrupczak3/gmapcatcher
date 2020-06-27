# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that allows Export of entire locations to new tiles repository

import pygtk
import gobject
pygtk.require('2.0')
import gtk
from gmapcatcher.mapMark import MyMarkers


from gmapcatcher.mapConst import *

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class AddMarker(gtk.Window):
    def __init__(self, handler, pointer):
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

        def btn_ok():
            button = gtk.Button(stock=gtk.STOCK_OK)
            button.connect("clicked", btn_ok_clicked)
            hbox = gtk.HButtonBox()
            hbox.pack_start(button)
            hbox.set_layout(gtk.BUTTONBOX_SPREAD)
            return hbox

        def btn_ok_clicked(button):
            color = self._marker_color.get_active()
            handler(color,
                        str(self._marker_name.get_text()),
                        pointer)
            self.destroy()

        gtk.Window.__init__(self)
        hbox = gtk.HBox(False, 20)
        vbox = gtk.VBox(False, 5)
        hbox.pack_start(btn_ok())
        vbox.pack_start(hbox)
        vbox.pack_start(_color_debug())
        vbox.pack_start(_markerName())
        self.add(vbox)
        self.set_title("Add New Marker")
        self.set_border_width(10)
        self.show_all()
