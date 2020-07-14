# Intersection_Fixer
Maya script for finding and fixing intersecting polygons

Idea behind it:

From the day that I started working on low poly characters and creating hair planes for them I frequently had to fix overlapping polygons. I needed to fix those intersections because otherwise I would have strange looking shading collisions. Therefore one day idea popped to build algorithm that would automatically detect intersecting polygons and move them so it would automatically fix model and won`t create big distortions or weird shapes. 
After doing some research I actually found mel script in Koshigaya script package which kind of did what I wanted, although it just detected overlapping faces and it was written in mel. I took it as a base and rewrote everything in python and used numpy library. I was trying to avoid Maya API and wanted to improve my math knowledge. Although Maya API would have definitely speed up calculation time.
Completed intersection finding algorithm I faced with much bigger complexity. I needed to find a way to move intersecting face vertices in the right directions, taking in account overall plane shape and normals. Otherwise it would have created even more intersections or it would have moved vertices in the wrong directions causing to hide themselves behind other faces which on the contrary needed to be on the top. Experimenting took me some time although I eventually found out that I definitely need more complex math knowledge and spend more time on it than I expected. Therefore I left it quite basic. I did an algorithm which takes intersecting edge, finds it`s start and ends points, checks which point is closest to intersection point and moves that line point into intersection point with offset that user can control. 
It might solve a really small portion of cases, but I am leaving it for now as it is and maybe after some time I will come back to update it with deeper math knowledge and fresh eyes.


Working example:

<a href="https://gifyu.com/image/QVf7"><img src="https://s7.gifyu.com/images/Intersection_finder_V01.gif" alt="Intersection_finder_V01.gif" border="0" /></a>
