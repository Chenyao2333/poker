#! /bin/bash

rm -rf /tmp/louch
./package.py /home/louch
rm -rf /tmp/louch.tar.gz
cd /tmp
tar cvfz /tmp/louch.tar.gz louch

