# Video Cutter Instructions

*Video Cutter (vcut)* is a command-line program to help you quickly chop large video files into smaller and more manageable segments for use in your video editor (or publish directly if you wish). It uses *ffmpeg* to do *stream copies* and does not engage any video encoders. This makes the process very fast and not CPU-intensive. However, it means that *ffmpeg* will choose the first I-frame (keyframe) before your cut points to actually make the cuts, which could be several seconds prior. This tool is a chainsaw, not a scalpel.

## Terminology

| Term | Meaning |
| --- | --- |
| Cut Point | A point in the video in which you wish to make a cut. |
| Segment | A span of video demarcated by cut points. There will always be one more segment than cut points. |
| Keeper | A segment you wish to keep. By default all segments are kept. |
| Job | The list of commands used to invoke *ffmpeg* to achieve the desired results |
| I-frame (or keyframe) | An encoded image which acts as a starting point frame for the video compressor |

## Usage

Usage is as follows:

`vcut <infile> cutpoints...`

... or ...

`vcut <infile> cutpoints... -k keepers...`

The second method will tell vcut to keep only certain segments demarcated by the cut points you provide. All cut points are specified with a standard-ISO-like time notation such as `00:12:34` or `00:12:34.567`. You must use hours, minutes, and seconds for each point. Using only two fields has strange and likely unwanted behavior, such as specifying hours and seconds. Note that since *ffmpeg* will cut the file at the nearest I-frame, specifiying milliseconds or microseconds (six digits after the decimal) -- also technically legal -- will be lost precision.

You can also just get the job itself in the form of text output to the console with the `-j` flag.

```vcut <infile> cutpoints... -k keepers... -j```

This will print the commands generated to invoke *ffmpeg* instead of actually invoking them. You could redirect this to a file, edit the commands if you wish, and add the sh'bang and set it executable as necessary for your platform, and then run it as a script. It's also a good way to see what this program *really* does.

### Examples

`vcut 'kittens.mkv' 00:09:30 00:14:50`

This will produce three videos. The first being from the beginning of the video to `00:09:30`, the second from `00:09:30` to `00:14:50`, and the last one from `00:14:50` to the end of the video.

`vcut 'V7GJ2230.MP4' 00:06:00 00:35:00 01:41:00 02:17:00 -k 1 3`

This will cut the video into five segments and copy two of them. The first is the segment from `00:06:00` to `00:35:00` and the second one will be from `01:14:00` to `02:17:00` and the rest will not be produced. The list of *keeper* indices is 0-based, meaning that the first one is `0`. The original file is not deleted.

### Output

A folder will be created in the current working directory that has the base name of the input file with `.cuts` concatenated to it. Produced files, as well as a digest of the `stderr` outputs from each invokation of *ffmpeg* will be placed in this folder. If that folder already exists, the program will refuse to run, instead instructing you to do something with the output of the previous invokation.

```py
self.outfolder = path.join(getcwd(), f"{i_fbase}.cuts")
```

