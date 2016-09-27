# Hello, my friends!

Football stats is a system which has the purpose of helping football match analyses. The final goal of the project is to have the capability of ball and players' position analysis, creating heatmaps and statistics of different actions or situations.

# How do I start the demo?

1. Install Python and PIP (if not already included)
2. Install necessary libraries: `pip install <missing_library>` (you would most probably need to install the following libraries: imutils, numpy, cv2)
3. Install OpenCV:
    * for Windows: http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html
	* for Mac:
		+ install homebrew (http://brew.sh)
		+ `brew tap homebrew/science`
		+ `brew install opencv`
4. Start the demo with:
	* `python main.py --video <path_to_video_file>` - for usage with pre-recorded video file
	* `python main.py` - for using the camera's live feed as source
5. Once the script is running it will freeze at the first frame, and wait for you to provide four points on the screen (by left-button clicks with the mouse)
6. Enjoy!

## Project history and background info

This project was born as part of an initiative of doing short 5-day sprints on trying to solve some problem.

### Day 1

We started with a rough idea and we needed to clear up the details to get started. After a few short meetings of the project's team members, we set ourselves some more clear goals for this project:
* player movement heatmaps
* point-in-time snapshots
* statistics and reports on player speed, acceleration, heart rate, total shots, shots on target, passes (attempted,completed), ball possession percentage, corners, goal kicks, throw-ins.

After a short discussion we decided that this Sprint-1 goals should be achievable, so that by Day-5 we could have something working as a prototype to get us started and provide validation of our idea. Then we could build on this in future phases of the project.

Sprint-1 scope:
Build a proof-of-concept demo for detecting a player on the screen/field, track their movement and display it as a heatmap.

During some quick brainstorming sessions we drew a list of potential technologies, which could prove useful for identifying and determining a player and their position:
* GPS
* Image processing / computer vision
* IR detection
* 3D reconstruction
* Bluetooth/WiFi signal strength trilateration
* Ultrasonic sensors
* Laser detectors

We split the list of technologies/topics and did some research on them for the rest of the day one and half of day two. The idea was to gain some more insight into these topics and assess their usefulness for our project.

### Day 2

After the research was done, we made a discussion and did a summary on each technology's pros/cons. As a result we chose one of them to use in our project.
* GPS - Consumer-grade devices do not provide good enough precision (errors of up to 4-8 meters, position update only 1 per second); there are higher-grade solutions, but they would require too much investment and energy for our iniatial goals of this project.
* CV - A set of software technologies and algorithms for interpreting the visual information provided by images/videos. A bit steppig stone for in this field is the OpenCV library, which made CV a good candidate technology for our project's initial goals.
* IR - Possible usage by attaching IR transmitters with varying wavelength on each player, and detect/recognise players by using different filters on the video; while not perfect, this approach deserves to be given a try, but probably not in this first phase, as we would lose the focus of the idea if we build the prototype in sprint one.
* 3D - In short: taking a stereo image (shot with 2 cams, at least) and building a depth map; a nice technology, but would probably makе tracking a moving object very CPU intensive, and it'd probably be more suitable for precise reconstruction of a 3D object
* BT - The idea was to try to determine player position by having them transmit BT signal (wristbands?) and have BT receivers around the field measure signal strength; Then by doing trilateration a player's position could be determined; However, after initial tests it turned out that BT signal degrades seriously at more than 4-5 metres and distance-to-signal strength mappings can be very hard to make; This meant that we would have to place BT receivers every 5 (at most 10) meters across the entire field; Not good. 
* US - Cheap and easy to obtain technology for distance measurement; BUT reasearch shows that consumer-grade UltraSonic sensors provide adequate accuracy in up to 6-10 metres at best; Moreover, not suitable for noisy environments.
* LZ - Cool technology, capable of high precision, long range distance measurement; the drawback is that it requires that the laser is pointed directly towards the measured object, meaning that the laser detector should somehow be attached to some mechanical construction which track the player and points the laser toward them. So things get a bit complicated. Moreover, such an implementation would require an array of lasers and/or complicated moving mechanics.

At the end of the day, we decided to focus our efforts on computer vision and image processing with OpenCV.

### Day 3

We marked the potential computer vision departments we wanted to dive into, so that we could achive our current goal of creating a prototype solution capable of detecting a player on the screen and track their movement. We split the tasks in 3 groups:
* Player detection / motion tracking
* Player identification
* Player camera to field coordinates projection

We once again split the tasks among the members of the team and started getting to know the OpenCV library's capabilities with the Python language - both of which were new to us.

### Day 4

After reading some OpenCV docs and playing around with code examples, we had built some background and had a better understading of the library's capabilities. We shot some sample videos (one or more of us holding a sheet of paper with number on it and moving around the backyard at the office) and started our attempts at creating a working prototype by using the videos for testing the algorithms. Here are some of the things we thought that would be useful:
* motion detection and tracking by background-foreground subtraction
* text/letter/digit recognition for identifying the player by the shirt number
* functions for creating transformation matrixes for converting perspective view coordinates to top-view 2D coordinates of the field.

We also identified some cases and potential objects on the field which would not be addressed at this phase:
* tracking/detecting a player behind another one - in future phases of the project, we are planning on using more than one camera for shooting at different angles to overcome these issues. The presence of two or more cameras would require, collecting and processing the video information from all sources at a single computer and synchronizing it. By doing this, we would also be able to obtain more precise coordinates by calculating average position from all the sources.
* referee identification and tracking
* ball detection and tracking

### Day 5

The last day of this sprint. At the start of the day, most of the components of our prototype were almost ready. Only the player recognition/identification was still a problem. It turned out that the letter/digit recognition algorithms required a lot more samples (different angles, proportions) than we expected for teaching the system how to correctly recognise them. We also tried out [FLANN](http://docs.opencv.org/2.4/doc/tutorials/features2d/feature_flann_matcher/feature_flann_matcher.html) based tracking algorithms, but the results were even more inaccurate, especially when there was too many details in the video. It seems that we would need a lot more research on the topic for other ways of doing the identification (or at least more time to improve the results with the current ones), so this functionality is missing in the current prototype/demo. As for the other topics:
* we fine-tuned the logic for getting the player position coordinates by creating an algorithm for calculating running average of the last 10 positions (this is usually from the last 10 frames of the video)
* false-positive object detections - by ignoring objects which are too small (area) or outside the borders of the field
* drawing a rectangle around the moving player/object
* interactions to provide the initial 4 points with mouse clicks (instead of hard-coding the field's coorinates in the code)


### Sprint-1 Summary

At the end of the day, we had a working prototype which was capable of tracking the player's movement and creating a 2D view heatmap. This was done by using motion tracking algorithms (generally background-foregraound subtractions), getting the base of the object as a position and traslating the perspective view coordinates to 2D one, thus creating a heatmap. After doing some real-world on-site measurements by using some by-standing objects as reference, calculations showed that the accuracy of the coordinates was correct up to a few centimeters. As for the player identification - the library's feature matching capabilities that we tried were not doing a good enough job for this use even after a lot of fine-tuning. So the letter/digit recognition algorithms definitely have a better potential, although they require a lot of samples (pictures) of the digits in order to teach the system to accurately recognise them.

### What next?

Definately the first step for the next phase (Sprint-2) should be the successful player identification/recognition - who's the player and which team he's on - that would be a good challenge with a lot of options still to be tried out. Once we achieve this goal, that would open the door for creating logic for the following steps:
* tracking more than one player
* predict a player's position, even if he's not recognisable from the current view/camera
* sync and proccess frames from multiple video sources
* ball detection and tracking
* referee and other non-player detection (medical staff, a fan running around :) ..., etc.)
* algorithms for recognising various event or player interactions (passes, shots, fouls, goals, throw-ins, goal kicks, corners, etc.)

So the door is open for Sprint-2, with lots of new challenges to take on and territories to explore!