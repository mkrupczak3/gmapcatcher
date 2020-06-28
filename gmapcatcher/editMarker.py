# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.widTreeView
# EditMarker class provides read write file functionality, which has been coppied from widTreeView.py file

import gtk
import gmapcatcher.fileUtils as fileUtils
from gmapcatcher.mapConst import *

class EditMarker():
    ## Appends items to a list from the given file
    def read_file(self, strInfo, strFilePath, listStore):
        locations = fileUtils.read_file(strInfo, strFilePath)
        # add rows with text
        if strInfo == "marker":
            if locations:
                for strLoc in locations.keys():
                    listStore.append([strLoc, locations[strLoc][0],
                                      locations[strLoc][1], locations[strLoc][2], locations[strLoc][3]])
        else:
            if locations:
                for strLoc in locations.keys():
                    listStore.append([strLoc, locations[strLoc][0],
                                      locations[strLoc][1], locations[strLoc][2]])
        return listStore

    ## Writes a given list to the file
    def write_file(self, strInfo, strFilePath, listStore):
        locations = {}
        if strInfo == "marker":
            for row in listStore:
                locations[row[0]] = (float(row[1]), float(row[2]), int(row[3]), int(row[4]))
        else:
            for row in listStore:
                locations[row[0]] = (float(row[1]), float(row[2]), int(row[3]))
        fileUtils.write_file(strInfo, strFilePath, locations)
