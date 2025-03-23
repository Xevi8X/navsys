#!/bin/bash

FLIGHTGEAR_EXECUTABLE="fgfs"
FLIGHTGEAR_OPTS="""--fg-aircraft=`pwd`/fg
--aircraft=uav
--timeofday=noon --airport=EPBC --runway=28L --altitude=500 --enable-terrasync
--disable-sound --disable-random-objects --prop:/sim/gui/menubar=false
--geometry=1280x720 --fov=75
--prop:/sim/gui/menubar/autohide=true
--prop:/sim/traffic-manager/enabled=0
--fdm=null --max-fps=30  --native-fdm=socket,out,30,localhost,5501,udp --native-fdm=socket,in,30,localhost,5502,udp"""

$FLIGHTGEAR_EXECUTABLE $FLIGHTGEAR_OPTS > /dev/null 2>&1 &
FLIGHTGEAR_PID=$!
echo "FlightGear PID: $FLIGHTGEAR_PID"

sleep 1

FLIGHTGEAR_XID=$(wmctrl -l | grep "FlightGear" | awk '{print $1}')
echo "FlightGear Window ID: $FLIGHTGEAR_XID"

# gst-launch-1.0 ximagesrc xid=$FLIGHTGEAR_XID ! videoconvert ! x264enc tune=zerolatency speed-preset=ultrafast ! rtph264pay ! udpsink host=127.0.0.1 port=5000 sync=false async=false > /dev/null 2>&1 &
gst-launch-1.0 ximagesrc xid=$FLIGHTGEAR_XID ! videoconvert ! videorate ! video/x-raw,framerate=15/1 ! x264enc tune=zerolatency speed-preset=medium bitrate=5000 qp-min=18 qp-max=30 ! rtph264pay ! udpsink host=127.0.0.1 port=5000 sync=false async=false > /dev/null 2>&1 &


GSTREAMER_PID=$!
echo "GStreamer PID: $GSTREAMER_PID"

wait $FLIGHTGEAR_PID