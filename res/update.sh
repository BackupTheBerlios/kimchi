#!/bin/bash

# translate
pylupdate4 -verbose kimchi.pro
lrelease -verbose kimchi.pro

# update resource 
pyrcc4 -verbose -o ../src/ui/resources.py resources.qrc

