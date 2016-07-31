import os
from bluepy.btle import Scanner
from storage import RemoteDataStore
from scan import DeviceForwardingDelegate
from tokencube import TokenCubeHandler

__author__ = "Leo Gaggl"
__copyright__ = "Copyright 2016, Leo Gaggl"
__credits__ = ["Tore Birkeland"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Leo Gaggl"
__email__ = "leo@gaggl.com"
__status__ = "Prototype"

#TODO: Move to config file 
device_settings = {
    "f1:11:11:11:10:11": {
        "device": "TokenCube 1",
        "addr": "f1:11:11:11:10:11",
        "type": "ambient"
    },
    "f1:11:11:11:10:12": {
        "device": "TokenCube 2",
        "addr": "f1:11:11:11:10:12",
        "type": "ambient"
    }
}

if __name__ == "__main__":
    
    print "Creating Scanner"
    delegate = DeviceForwardingDelegate()
    delegate.handlers.append(TokenCubeHandler(device_settings))

    scanner = Scanner()
    scanner.withDelegate(delegate)
    
    print "Connecting to Buddy server"
    storage = RemoteDataStore()
    storage.get_access_token()
    storage.configure_telemetry()

    while True:
        print "Reading sensors..."
        scanner.scan(30)
        print "Storing data..."
        for handler in delegate.handlers:
            handler.store_data(storage)
		
