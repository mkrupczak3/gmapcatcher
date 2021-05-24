# rafasaurus patches

# Added functionalities Left click menu #

## Calculate Azimuth ##
given two positions (selected by left click), show azimuth angle, distance, sk42 coordinates
<img src="https://github.com/rafasaurus/gmapcatcher/blob/master/images_doc/calculate_azimuth.png" width="50%" height="50%">

## Show elevation profile ##
given two positions (selected by left click), plot elevation profile using elevation data from .GMapCatcher/elevation.tiff
<img src="https://github.com/rafasaurus/gmapcatcher/blob/master/images_doc/elevation_profile.png" width="50%" height="50%">

## Sk42Calculator ##
just interactable simple sk42calculator for general usage

## Edit marker ##
move the nearest marker from mouse position

## Calculate intersection ##
given two camera positions (selected by left click), insert predefined azimuth angles (insertable) of cameras, calculate the target
<img src="https://github.com/rafasaurus/gmapcatcher/blob/master/images_doc/calculate_intersection.png" width="50%" height="50%">
# Modified functionalities #

## Add marker from left click menu
ability to add markers using input cordinates, both wgs84 and sk42
ability to change marker color
<img src="https://github.com/rafasaurus/gmapcatcher/blob/master/images_doc/add_marker.png" width="50%" height="50%">

## Add marker with current point
first select the marker with left click then use "add marker with current point" from right click menu
given compass angle and distance, it will caluclate and insert new marker's position 
<img src="https://github.com/rafasaurus/gmapcatcher/blob/master/images_doc/add_marker_with_current_point.png" width="50%" height="50%">

## Getting the elevation data ##
download geotiff from https://search.earthdata.nasa.gov/
merge multiple geotiffs with oqgis" software, output file must be elevation.tiff in .GMapCatcher

### troubleshooting packages ##
for arch linux "import gobject" install "python2-gobject2" package with pacman

## Overview ##

GMapCatcher is an offline maps viewer. It can display maps from many providers such as:

[CloudMade](http://maps.cloudmade.com/), [OpenStreetMap](http://www.openstreetmap.org/), [Yahoo Maps](http://maps.yahoo.com/), [Bing Maps](http://www.bing.com/maps/), [Nokia Maps](http://maps.nokia.com), ~~SkyVector~~, ~~Google Map~~.

It displays them using a custom GUI. User can view the maps while offline. GMapCatcher doesn't depend on the map's JavaScript.

GMapCatcher is written in Python 2.7 & PyGTK, can run on Linux, Windows and Mac OSX.

![https://raw.githubusercontent.com/heldersepu/gmapcatcher/wiki/snapshot.gif](https://raw.githubusercontent.com/heldersepu/gmapcatcher/wiki/snapshot.gif)

You can find a list of improvements and latest features in the [Changelog](https://github.com/heldersepu/GMapCatcher/blob/master/changelog.md)

## Download ##

https://github.com/heldersepu/GMapCatcher/releases

or

```
$ git clone https://github.com/heldersepu/gmapcatcher
```


## Usage ##

See the [User Guide](https://github.com/heldersepu/GMapCatcher/blob/wiki/User_Guide.md) for more details.


**maps.py** is a gui program used to browse google map. With the **offline** toggle button unchecked,  it can download google map tiles automatically. Once the file downloaded, it will reside on user's hard disk and needn't to be downloaded again any more, there is an optional "Force update" if the tile is older than 24 hours, it will be re-downloaded.

**download.py** is a downloader tool that can be used to download map tiles without gui. **maps** can use files it downloaded without configuration.

Below is an example using **download.py**:
```
$ download.py --location="Paris, France" --max-zoom=16 --min-zoom=0 --latrange=2.0 --lngrange=2.0
```

## Files ##
Linux:
```
$HOME/.GMapCatcher/*
```

Windows:
```
%UserProfile%/.GMapCatcher/*
```

## Dependencies ##

Windows users are highly recommended to download the [latest Windows installer](https://github.com/heldersepu/GMapCatcher/releases).
This installer contains all required packages, works well on XP, Vista, Win 7, 8 & 10 .
For a complete list of tested OS, see wiki [Tested Operating Systems](https://github.com/heldersepu/GMapCatcher/blob/wiki/TestedOperatingSystems.md).


If you choose to run directly from sources you must have all dependencies, see wiki: 
https://github.com/heldersepu/GMapCatcher/blob/wiki/devEnv.md
or see [win_install](win_install.md) for windows.

