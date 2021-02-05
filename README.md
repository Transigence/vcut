# Video Cutter (vcut)
 
*Video Cutter* is currently a command-line program that assists in cutting video files into manageable segments. A GUI version is in the works, but it is still a ways off.

## Raison D'être

Non-linear video editors (NLEs) are great for making precision cuts, adding transitions, textual titles, animations, particles, speed changes, subtitles, pictures-in-picture and any number of other things in order to produce a highly-refined finished product from raw takes. But where they fall short is in providing a good worflow for making coarse primary cuts to very large files. When you load a file into an NLE and move it to the timeline, most editors immediately start producing a shadow file to allow for quick scrubbing with a preview window. While this is preferable to scrubbing through the actual video file, it takes a lot of work for your CPU to produce and takes up quite a bit of hard drive space. If you know that you're only going to use a very small fraction of the source video file, this is a waste of time and resources. Furthermore, if you have a very long video file in your timeline the interface can become difficult to use. You are either zoomed out such that your clip fits in the timeline but very slight movements cause huge changes, or you're zoomed in such that the clip has a very long representation. The purpose of *Video Cutter* is to quickly chop these files down into more manageable segments in a single stroke without engaging any encoders, thereby making the process very fast and preserving original quality. This will yield much more manageable primary assets for your video production task.

## Caveats

There are a few caveats to this program in its current state. They are:

1. You need to do some setup on your own.
    - *Video Cutter* relies on *FFMPEG* to do the heavy lifting. It will have to be installed and in the search path somewhere.
    - Python interpreter is required. It would also be helpful if Python is also in the search path.
2. The cuts are not made precisely where you ask for them.
    - One of the consequences of not engaging any encoders is that ffmpeg will only cut a video at the nearest keyframe before the point where you ask it to cut.
    - Precise cuts will be an option in future versions, but they will require engaging the encoder (this will also add flexibility in choosing/changing the file output)
3. It may not work with all codecs and all container formats.
   - It is only tested with h.264 streams in mp4 and mkv containers. It should work with any codec that can be stream-copied.
   - Right now it uses the same container format for the output as the input, but recontainerization will be an option added soon.
   - Output options are not flexible at this time. See the manual for details.
 
## Who should use this program?

This program is aimed at anyone who handles really long takes, such as gamers recording long playthroughs, or journalists who will end up with hours of footage to comb through for production later, or video producers who do this work professionally and want an extra tool to streamline their workflow.
