#-------------------------------------------------------------------------------
# Name:        NetstatMonitor.py
# Purpose:
#
# Author:      shreyas shinde
#
# Created:     08/10/2013
# Copyright:   (c) shreyas shinde 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os;
from subprocess import Popen, PIPE;
from time import sleep;
import sys;
import datetime as dt;

def printUsage():
    ''' Prints usage '''
    print "NetstatMonitor <search_String> [sleep_seconds]";
    sys.exit(1);


def main():
    ''' Searches the output of the netstat command for a specific string'''
    print sys.argv
    if len(sys.argv) <= 1:
        printUsage();
        return;

    # get search string
    searchString = sys.argv[1];
    sleepTime = 60; # 1 minute
    if len(sys.argv) == 3:
        sleepTime = int(sys.argv[2]);

    while True:
        # exec netstat
        result = Popen("netstat -p tcp", stdout=PIPE, shell=True).stdout.read();
        # count occurance of search string
        print "Search string '" + searchString + "' occurred " + str(result.count(searchString)) + " times in the netstat result @ "  + str(dt.datetime.now()) + ".";
        sleep(sleepTime);


if __name__ == '__main__':
    main();
