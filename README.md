# Video Cutter (vcut)
 
*Video Cutter* is currently a command-line program that assists in cutting video files into manageable segments. A GUI version is in the works, but it may be quite some time before it is ready.

## Raison D'être

Non-linear video editors (NLEs) are great for making precision cuts, adding transitions, textual titles, animations, particles, speed changes, subtitles, pictures-in-picture and any number of other things in order to produce a highly-refined finished product from raw takes. But where they fall short is in providing a good workflow for making coarse primary cuts to very large files. When you load a file into an NLE and move it to the timeline, most editors immediately start producing a shadow file to allow for quick scrubbing with a preview window. While this is preferable to scrubbing through the actual video file, it is processor intensive to produce and takes up a lot of hard drive space. This is a waste of time and resources. Furthermore, if you have a very long video file in your timeline the interface can become unwieldy. The purpose of *Video Cutter* is to quickly chop these files down into more manageable segments in a single stroke without engaging any encoders, thereby making the process very fast and preserving original quality. This will yield much more manageable primary assets for your video production task.

## Caveats

There are a few caveats to this program in its current state. They are:

1. You need to do some setup on your own.
    - *Video Cutter* relies on *ffmpeg* to do the heavy lifting. It must be installed and in the search path somewhere.
    - The *Python 3* interpreter is required. It would also be helpful if *Python* is also in the search path, and optionally for `.py` files to be listed in your `PATHEXT` environment variable if you are on Windows.
2. The cuts are not made precisely where you specify them.
    - One of the consequences of performing a *stream copy* is that *ffmpeg* will only cut a video at the nearest I-frame before the point you specify to cut.
    - Precise cuts will be an option in future versions, but they will require engaging the encoder. However, this will also add flexibility in choosing/changing the file output.
3. It may not work with all codecs and all container formats.
   - It is only tested with h.264 streams in mp4 and mkv containers, although it should work with any codec and container that can be stream-copied.
   - Right now it uses the same container format for the output as the input, but recontainerization will be an option added soon.
   - Output options are not flexible at this time. See the manual for details.
4. It is not yet bullet-proofed.
 
## Who should use this program?

This program is for anyone who handles long video files. Independent journalists, video producers, and gamers recording long playthroughs will benefit from using this program the most. It's quite possible that security personnel handling day-long and week-long surveillance video files may also find some use for it.
