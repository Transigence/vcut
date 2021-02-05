# Video Cutter Instructions

*Video Cutter (vcut)* is a command-line program to help you quickly chop large video files into smaller and more manageable segments for use in your video editor (or publish directly if you wish). It uses FFMPEG to do *stream copies* and does not engage any video encoders. This makes the process very fast and not CPU-intensive. However, it means that FFMPEG will choose the first I-frame before your cut points to actually make the cuts, which could be several seconds off. This tool is a chainsaw, not a scalpel.

## Usage

Usage is as follows:
`vcut <infile> cutpoint ...`
... or ...
`vcut <infile> cutpoint ... -k kept ...`
The second method will tell vcut to keep only certain segments demarcated by the cut points you provide. All cut points are specified with a standard-ISO-like time notation such as `00:12:34` or `00:12:34.567`. You must use hours, minutes, and seconds for each point. Using only two has strange behavior like specifying hours and seconds.

### Terminology

| Term | Meaning |
| --- | --- |
| Cut Point | A point in the video in which you wish to make a cut. |
| Segment | A span of video demarcated by cut points. There will always be one more segment than cut points. |
| Keeper | A segment you wish to keep. By default all segments are kept. |

### Examples

`vcut 'kittens.mkv' 00:09:30 00:14:50`

This will produce three videos. The first being from the beginning to `00:09:30`, the second from `00:09:30` to `00:14:50`, and the last one from `00:14:50` to the end of the video.

`vcut 'V4GJ2230.MP4' 00:06:00 00:35:00 01:41:00 02:17:00 -k 1 3`

This will cut the video into five segments and keep the segment from `00:06:00` to `00:35:00` and the second being from `01:14:00` to `02:17:00` and discard the rest. The list of *keeper* indices are 0-based, meaning that the first one is `0`. It is worth noting that the original file is not deleted so nothing is truly "discarded" per se, it's just never created in the first place.
