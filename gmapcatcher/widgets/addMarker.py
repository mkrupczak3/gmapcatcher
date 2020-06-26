# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that allows Export of entire locations to new tiles repository

import pygtk
pygtk.require('2.0')
import gtk
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

            self.store = gtk.ListStore(str)
            self.store.append(["green"])
            self.store.append(["red"])
            self.store.append(["blue"])
            self.store.append(["yellow"])

            self.entry = gtk.ComboBoxEntry(self.store)

            self._marker_color = self.entry
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame(" Color", vbox)

        def btn_ok():
            button = gtk.Button(stock=gtk.STOCK_OK)
            button.connect("clicked", btn_calculate_clicked)
            hbox = gtk.HButtonBox()
            hbox.pack_start(button)
            hbox.set_layout(gtk.BUTTONBOX_SPREAD)
            return hbox

        def btn_calculate_clicked(button):

            if self._marker_color.get_active_text == "green":
                color = MARKER_GREEN
            elif self._marker_color.get_active_text() == "blue":
                color = MARKER_BLUE
            elif self._marker_color.get_active_text() == "yellow":
                color = MARKER_YELLOW
            else:
                color = MARKER_DEFAULT_COLOR
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
