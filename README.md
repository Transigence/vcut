# Video Cutter (vcut)
 
*Video Cutter* is currently a command-line program that assists in cutting video files into manageable segments. A GUI version is in the works, but it is still a ways off.

## Raison D'être

Non-linear video editors (NLE) are great for making precision cuts, adding transitions, textual titles, animations, particles, speed changes, subtitles, pictures-in-picture and any number of other things in order to produce a highly-refined finished product from raw takes. But where they fall short is in providing a good worflow for making coarse primary cuts to very large files. When you load a file into an NLE and move it to the timeline, most editors immediately start producing a shadow file to allow for quick scrubbing with a preview window. While this is preferable to scrubbing through the actual video file, it takes a lot of work for your CPU to produce and takes up quite a bit of hard drive space. If you know that you're only going to use a very small fraction of the source video file, this is a waste of time and resources. Furthermore, if you have a very long video file in your timeline the interface can become difficult to deal with. You are either zoomed such that you your clip fits in the timeline, in which case very slight mouse movements cause huge jumps in the scrub head position, or you're zoomed such that the mouse makes moderate moves in the scrub head, but the clip has a very, very long representation. The purpose of *Video Cutter* is to quickly chop these files down into more manageable segments in a single stroke, without engaging any encoders, before you ever load it into your NLE in the first place. If your raw take is more than an hour long but you know for certain that you are only going to use a few minutes from it, then it is much easier to have already cut those segments out from the source file.

## Caveats

There are a few caveats to this program in its current state. They are:

1. You need to do some setup on your own.
    - *Video Cutter* relies on *FFMPEG* to do the heavy lifting. It will have to be installed and in the path somewhere.
2. You will need Python installed.
    - It would also be helpful if Python was in the path as well.
3. The cuts are not made precisely where you ask for them.
    - One of the consequences of not engaging any encoders is that ffmpeg will 
only cut a video at the nearest keyframe before the point you as it to cut.
4. It may not work with all codecs and all container formats.
   - It is only tested with h.264 streams in mp4 and mkv containers.
 
## Who should use this program?

This program is aimed at anyone who handles really long takes, such as gamers recording long playthroughs, or journalists who will end up with hours of footage to comb through for production later, or video producers who do this work professionally and want an extra tool to streamline their workflow.
