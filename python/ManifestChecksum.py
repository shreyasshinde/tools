#-------------------------------------------------------------------------------
# Name:        ManifestChecksum
# Purpose:     This tools is capable of producing a manifest of files in directory
#              and then run a checksum on a new installation to make sure if the
#              new installation (directory) is within a tolerance of the manifest.
#
# Author:      shreyas shinde
#
# Created:     20/08/2013
# Copyright:   (c) shreyas shinde 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys;
import getopt;
import os;
import datetime as dt;

def print_usage():
    print "ManifestChecksum [MODE] [OPTIONS] -d <directory>"
    print "-d <directory>: path to the directory on which to run the operation"
    print "MODE:"
    print "\t -m: produces a manifest on the given directory"
    print "\t -c: runs a checksum on the given directory"
    print "OPTIONS:"
    print "for manifest mode (-m)"
    print "\t -f <file>: path to file that will contain the manifest file"
    print "for checksum mode (-c)"
    print "\t -f <file>: path to file that contains the manifest"
    print "\t -t <tolerance>: the % tolerance between the size of files"
    print "\t -o <file>: path to the file that contains the report of the checksum"

def manifest():
    ''' Produces a manifest by browsing a directory '''
    print "Manifest mode";
    optlist, args = getopt.getopt(sys.argv[1:], "mf:d:");
    f = "";
    searchPath = "";
    for o, a in optlist:
        if o == "-f":
            f = a;
        if o == "-d":
            searchPath = a;

    # file to write the manifest
    manifestFile = open(f, "w");
    manifestFile.write("# manifest created on: " + str(dt.datetime.now()) + " for directory path: " + searchPath + "\n");
    manifestFile.write("\n");

    # file count
    fileCount = 0;

    # walk the dir path
    for (dirpath, dirnames, filenames) in os.walk(searchPath):
        # iterate over every dir and write its files out
        for filename in filenames:
            # get file stats
            fullPathToFile = os.path.join(dirpath, filename);
            stat = os.stat(fullPathToFile);
            # normalize the path by removing the searchPath from the file name
            fullPathToFile = fullPathToFile.replace(searchPath, "");
            manifestFile.write(fullPathToFile + "," + str(stat[6]) + "\n") ;
            fileCount += 1;
    manifestFile.write("# Total files in manifest: " + str(fileCount) + "\n");
    manifestFile.close();
    print "Total files added to manifest: " + str(fileCount);
    return;


def checksum():
    ''' Validates if the input directory honors the manifest and returns the number of violations '''
    print "Checksum mode";
    optlist, args = getopt.getopt(sys.argv[1:], "cf:t:o:d:");
    mf = "";
    searchPath = "";
    tolerance = 0;
    report = "";
    for o, a in optlist:
        if o == "-f":
            mf = a;
        if o == "-d":
            searchPath = a;
        if o == "-t":
            tolerance = int(a);
        if o == "-o":
            report = a;

    # an in-memory manifest
    manifest = {};

    # a dictionary object to track files that violate the manifest
    violate = {};

    # load the manifest file in memory
    file = open(mf, "r");
    for line in file:
        line = line.strip();

        # ignore comments in manifest file
        if line == None or line == "" or line.startswith("#"):
            continue;

        # split the line into path and file size
        [path, size] = line.split(",", 1);
        manifest[path] = long(size);

    file.close();

    # count of processed files
    fileCount = 0;

    # walk the dir path
    for (dirpath, dirnames, filenames) in os.walk(searchPath):
        # iterate over every dir and write its files out
        for filename in filenames:
            # get file stats
            fullPathToFile = os.path.join(dirpath, filename);
            stat = os.stat(fullPathToFile);
            # normalize the path by removing the searchPath from the file name
            fullPathToFile = fullPathToFile.replace(searchPath, "");

            # test
            if fullPathToFile in manifest:
                expected = manifest[fullPathToFile];
                lower = expected*(100-tolerance)/100;
                upper = expected*(100+tolerance)/100;
                actual = stat[6];
                if (actual < lower) or (actual > upper):
                    violate[fullPathToFile] = actual;
            else:
                violate[fullPathToFile] = stat[6];

            fileCount += 1;

    # write the report
    reportFile = open(report, "w");
    reportFile.write("# checksum performed on: " + str(dt.datetime.now()) + " for directory path: " + searchPath + " with manifest file: " + mf + "\n");
    reportFile.write("# tested: " + str(fileCount) + "\n");
    reportFile.write("# violations: " + str(len(violate)) + "\n");

    for key,value in violate.iteritems():
        reportFile.write( key + "," + value);
    reportFile.close();
    return len(violate);

def main():
    if len(sys.argv) <= 1:
        print_usage();
        sys.exit(-1);
    retVal = 0;
    if "-m" in sys.argv:
        manifest();
    elif "-c" in sys.argv:
        retVal = checksum();
    else:
        print "Error: Unknown mode"
        print_usage();
        sys.exit(-1);

    print "Done!";
    sys.exit(retVal);










if __name__ == '__main__':
    main()
