# Google Mapping the Caves of Missouri
The purpose of this project was to automate the translation of cave locations, encoded in PLSS textual land descriptions, into GPS coordinates for Google Maps.

## Some Background Info

In 1956, Dr. J. Harlen Bretz published the legendary *Caves of Missouri*.
In this book lies extensive information on many caves in Missouri, ranging from their names, brief histories, and even their locations!
But the locations are encoded using the archaic Public Land Survey System [1], created in 1785 and used quite extensively throughout the US until the development of the Universal Transverse Mercator [2] \(UTM\) coordinate system in the 1940s, and subsequently the World Geodetic System [3] \(which includes GPS\) in the late 1950s and onward.

## Where can I find *Caves of Missouri*?

I can't help you there.
This book has become a spelunker's collectible in the past 20 years, and even if you find a copy, it'll likely cost upwards of $200 while still falling apart at its spine.
Additionally, cave locations are kept private, and for good reason.
Starting in Spring of 2010, the Missouri Department of Natural Resources made 110 caves strictly off limits [4] due to the spread of white nose syndrome [5], a fungus that is fatal to bats indigenous to these caves.
And even if they weren't closed, too many people have desecrated Missouri's caves with empty beer cans, spray paint, and other rubbish, dampening the experience for those who adhere to the Leave No Trace [6] principle.
Although this project is open source, it's the input data that gives this project value.

## How does this project convert from PLSS to GPS?

There's actually a service called the Township Geocoder [7], created by the Bureau of Land Management for their GeoCommunicator publication website.
I learned about this service while working for the U.S. Geological Survey through some of my old timer colleagues.
This service is a bit archaic, but it got the job done.

## Why did you create this?

Back during the summer of 2013, just before I was to start my PhD, I was having a boring day.
At the time, I was a student developer / cartographic software engineer for the U.S. Geological Survey, but the project I was working on was undergoing quality assurance, so I had a bunch of free time to occupy.

My colleagues and I were chitchatting, older gentlemen who started with the USGS back in the early 1980s, about recreational things to do in Missouri.
I love to spelunk (explore caves), and upon mentioning it, one of them walked back to his cubicle to retrieve his copy of *Caves of Missouri*.
I was awestruck, and asked him if I could make a copy of the book for my digital library.

After reading through it, and being confused at the strange notation used throughout the book, he educated me on the PLSS and how it is used to indicate a region on *quad maps* (USGS quadrangle maps [8]\).
Since I didn't want to pull up a quad map every time I wanted to find a cave, I began investigating how to do it automatically, and how to interface with the cave locations in a user-friendly manner.
Like most things I develop, laziness drives my motivation to automate.

----

[1] https://en.wikipedia.org/wiki/Public_Land_Survey_System  
[2] https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system  
[3] https://en.wikipedia.org/wiki/World_Geodetic_System  
[4] http://www.stltoday.com/news/local/state-and-regional/bat-disease-forces-closure-of-missouri-caves/article_bb652913-c532-5d54-81de-7f43e9eb7ea4.html  
[5] https://mostateparks.com/advisory/60398/missouri-cave-advisory  
[6] https://lnt.org/  
[7] http://www.geocommunicator.gov/GeoComm/lsis_home/townshipdecoder/index.htm  
[8] https://en.wikipedia.org/wiki/Quadrangle_(geography)  
