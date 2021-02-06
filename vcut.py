#Copyright (C) 2021 Paul Johnson
#Contact: paul.m.w.johnson@protonmail.com

import sys, argparse
from datetime import timedelta
from os import path, getcwd, mkdir
import subprocess

__author__= "Paul Johnson"
__copyright__ = "Copyright (C) 2021 Paul Johnson"
__license__ = "Public Domain"
__version__ = "0.9.8.2"


"""
Because of reasons, it is necessary to use datetime.timedelta for the internals.
However, I wish the user to use something like a standard ISO string for specifying time intervals,
and no facilities did precisely what I wanted. Therefore, I had to write these. The highest order is hours,
which can exceed 24, but timedeltas are kept internally as days, seconds, and microseconds.
"""

#pathinfo = i_dname, i_fname, i_fbase, i_fext, i_fqp

class Job():
    def getpathinfo(s):
        fullpath = path.abspath(s)
        d, f = path.split(fullpath)
        b, e = path.splitext(f)
        return d, f, b, e, fullpath

    def iso_sanitize(s): #ffprobe gives durations ending in .00 format, which is unusable.
        h, m, sec = s.split(":")
        sec = "{:2.6f}".format(float(sec))
        return f"{h}:{m}:{sec}"

    def get_segments(cutpoints): #Convert cut times into interval spans between them
        segs = []
        p = cutpoints[0]
        for cp in cutpoints[1:-1]:
            seg = p, cp
            segs.append(seg)
            p = cp
        seg = p, cutpoints[-1]
        segs.append(seg)
        return segs

    def timedeltafromhms(hms):
        h, m, s = hms.split(":")
        if "." in s:
            sec = s.split(".")
            if len(sec[1]) == 6:
                us = int(sec[1])
            elif len(sec[1]) == 3:
                us = int(sec[1]) * 1000
            s = int(sec[0])
        else:
            s = (int(s))
            us = 0
            
        return timedelta(hours=int(h), minutes=int(m), seconds=s, microseconds = us)

    def hmsfromtimedelta(td):
        h = int(td.days * 24 + int(td.seconds / 3600))
        m = int((td.seconds % 3600) / 60)
        s = int(td.seconds % 60)
        us = int(td.microseconds)
        return f"{h:02}:{m:02}:{s:02}.{us:06}"

    def create_endslist(cp, endtime):
        if not isinstance(endtime, timedelta):
            raise TypeError("endtime must be an instance of timedelta")
        if not hasattr(cp, '__iter__'):
            raise TypeError("cp must be iterable")
        ends = list()  
        ends.append(timedelta()) #Start the list of cut points with a 0 timedelta
        
        for p in cp:
            ends.append(Job.timedeltafromhms(p))
        
        ends.append(endtime)    
        return ends

    def create_command(seg, pathinfo, outfolder):
        #Generate filename-friendly timespans for file naming
        i_fbase, i_fext, i_fqp = pathinfo[2], pathinfo[3], pathinfo[4]
        spanstart = Job.hmsfromtimedelta(seg[0]).split(".")[0]
        spanend = Job.hmsfromtimedelta(seg[1]).split(".")[0]
        spanstring = f"{spanstart}_{spanend}".replace(":", "-")
        o_fqp = (path.join(outfolder, f"{i_fbase}.{spanstring}{i_fext}"))
        
        return f"ffmpeg -ss {Job.hmsfromtimedelta(seg[0])} -to {Job.hmsfromtimedelta(seg[1])} -i \"{i_fqp}\" -c:v copy -c:a copy \"{o_fqp}\""
    
    def __iter__(self):
        yield from self.commands

    def __init__(self, infile, cutpoints, keepers=None):
        self.cutpoints = cutpoints        
        self.commands = list()
        self.log = str()
        pathinfo = Job.getpathinfo(args.i)
        i_fbase, i_fqp = pathinfo[1], pathinfo[4]
        self.outfolder = path.join(getcwd(), f"{i_fbase}.cuts") #getcwd might need to be changed for GUI version, and hoisted to __main__
        self.error = str()
        
        result = subprocess.run("ffprobe -i \"%s\"" % i_fqp, capture_output=True)
        endtime = Job.timedeltafromhms(Job.iso_sanitize(str(result.stderr).split("Duration: ")[1].split(",")[0])) #Extract the duration of the input file from ffprobe output.

        ends = Job.create_endslist(cutpoints, endtime) #Create cutpoint ends as timedelta objects
        
        #Validate and sort the list of ends
        for cp in ends[:-1]:
            if not cp < ends[-1]:
                self.error = f"Time argument out of bounds! ({cp} > {ends[-1]})"
                self.commands = None
                return

        segs = Job.get_segments(sorted(ends))
        
        ikeepers=list() #indices of keepers
        if not keepers:
            ikeepers=range(0, len(segs))
        else:
            for k in keepers:
                if not k < len(segs):
                    self.error = "You specified a segment that will not be produced (#%d of max: #%d)!" % (k, len(segs) - 1)
                    self.commands = None
                    return
                if not k in ikeepers:
                    ikeepers.append(k)
            ikeepers = sorted(ikeepers)
        
        for k in ikeepers:
            self.commands.append(Job.create_command(segs[k], pathinfo, self.outfolder))
    
    
HELP_EPILOG = """
Example: %(prog)s <infile> 00:05:00 00:10:00
Result: Breaks the file into three pieces at the two cut points and keeps all three

Example: %(prog)s <infile> 00:00:48 00:19:29 00:20:42 00:41:11 -k 1 3
Result: Breaks the file into 5 pieces, keeps the segments from 00:00:48 -> 00:19:29 and 00:20:42 -> 00:41:11, and discards the rest

Example: %(prog)s <infile> 00:05:00 00:10:00 00:15:00 -j
Result: Creates the commands to break the file into 4 pieces and prints them to the console.

NOTICE: You must use all three fields for times or you will get unwanted results!
Example: 00:00:00

NOTICE: ffmpeg cuts at the nearest I-frame before the specified time, so cut points can be off by several seconds. It is not likely that specifying milliseconds or microseconds will be useful in this version of VCut.
"""

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description ="Cut a video along a list of cut points. Optionally, keep only certain segments. Output is placed in a directory bearing the same base name as the input file.",
        epilog=HELP_EPILOG)
    argparser.add_argument("i", type=str, nargs='?', help="Input file")
    argparser.add_argument("cp", type=str, nargs='+', help="Cut points")
    argparser.add_argument("-k", type=int, nargs='+', help="Segment numbers to keep (0-based), as defined by cp")
    argparser.add_argument("-j", action='store_true', help="Output job commands to console instead of invoking them")
    
    args = argparser.parse_args()
    
    if not path.exists(args.i):
        print("Couldn't find \"%s\"" % args.i)
        sys.exit(1)
    if path.isdir(args.i):
        print("\"%s\" exists but it is a directory!" % args.i)
        sys.exit(1)
    
    job = Job(args.i, args.cp, args.k)
    
    if job.error:
        print("Something went wrong creating the Job object.\n\"%s\"\n" % job.error)
        sys.exit(1)

    if args.j:
        for command in job:
            print(command)
        sys.exit(0)    
        
    else:
        if path.exists(job.outfolder):
            print("Output folder already exists. Decide what to do with these files, then delete them from this location before trying again!")
            sys.exit(1)
        mkdir(job.outfolder)
        for command in job.commands:
            result = subprocess.run(command, capture_output = True)
            job.log += result.stderr.decode()
    
    lfile = open(path.join(job.outfolder, "vcut.log"), "w")
    lfile.write(job.log)
    lfile.close()
