# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.widComboBoxLayer
# ComboBoxLayer widget used to collect data to search

import gtk
from gmapcatcher.mapConst import *
from gobject import TYPE_STRING, TYPE_INT


## This widget is where we the available Layers
class ComboBoxLayer(gtk.ComboBoxEntry):

    def __init__(self, conf):
        super(ComboBoxLayer, self).__init__()
        self.connect('key-press-event', self.key_press_combo)
        self.child.connect('key-press-event', self.key_press_combo)
        self.conf = conf
        currentMap = self.populate()
        self.set_active(currentMap)

    def populate(self):
        store = ListStore()
        currentMap = 0
        bad_map_servers = self.conf.hide_map_servers.split(',')
        pref_map_servers = self.conf.order_map_servers.split(',')
        pos = len( pref_map_servers);
        mapId = 0;
        for mapSrv in MAP_SERVICES:
            mapName = MAP_SERVERS[mapSrv['ID']]
            if self.conf.oneDirPerMap:
                if not str(mapSrv['ID']) in bad_map_servers:
                    # Loop over all entries and store them according to their order position.
                    for ln in mapSrv['layers']:
                        if ln > 0:
                            w = mapName + " " + LAYER_NAMES[ln]
                        else: 
                            w = mapName
                        # orderPos is last element and modified if current layer has an assigned position.
                        orderPos = pos
                        for intOrderPos in range( len( pref_map_servers)):
                            print( "pref_map_servers" + pref_map_servers[ intOrderPos] + ":" + str(intOrderPos))
                            if w == pref_map_servers[ intOrderPos]:
                                orderPos = intOrderPos
                        print( w + ":" + str(orderPos))
                        store.insertAt( orderPos, w, mapSrv['ID'], ln)
                        if mapName == self.conf.map_service and ln == self.conf.save_layer:
                            currentMap = orderPos - 1
                        # increase pos if no defined order was used.
                        if pos == orderPos:
                            pos = pos + 1
                    mapId = mapId + 1
            else:
                if mapName == self.conf.map_service:
                    for ln in mapSrv['layers']:
                        store.add(LAYER_NAMES[ln], mapSrv['ID'], ln)
                        if ln == self.conf.save_layer:
                            currentMap = len(store) - 1
        self.set_model(store)
        self.set_text_column(0)
        store.set_sort_column_id(3, gtk.SORT_ASCENDING)
        return currentMap

    ## Handles the pressing of keys
    def key_press_combo(self, w, event):
        if event.keyval < 5000 or event.keyval in [65288, 65535]:
            self.combo_popup()
            return True

    ## Show the combo list if is not empty
    def combo_popup(self):
        if self.get_model().get_iter_root() is not None:
            self.popup()

    def refresh(self):
        self.child.set_text('')
        self.set_model(None)
        self.populate()


class ListStore(gtk.ListStore):
    def __init__(self):
        super(ListStore, self).__init__(TYPE_STRING, TYPE_INT, TYPE_INT, TYPE_INT)

    def insertAt( self, pos, str, int1, int2):
        iter = self.append()
        self.set(iter, 0, str)
        self.set(iter, 1, int1)
        self.set(iter, 2, int2)
        self.set(iter, 3, pos)
        
    def add( self, str, int1, int2):
        self.insertAt( self.__len__(), str, int1, int2)
