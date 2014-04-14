# Project Proposal
### By Charlie Fisher, Clement Miao, Sam Przezdziecki
=================
### Dataset
We are using Pitchf/x data, a pitch tracking system that tracks the velocity, movement, release point, spin, and pitch location for every pitch thrown in baseball, allowing pitches and pitchers to be analyzed and compared at a detailed level. 
We will be able to download this dataset using an R package, called "pitchRx", as explained in [the following article](http://cpsievert.wordpress.com/2013/01/10/easily-obtain-mlb-pitchfx-data-using-r/), and save it as a collection of csv files. 

### Data Exploration & ideal outcome
After getting the data, we will agreggate all of the pitches that each pitcher threw, and then perform a clustering analysis on different aspects of their pitching style: pitch type, velocity, pitch break, ect. From this, we will be able to group similar pitchers together, and determine how similar they are to one another. Once we have this, we can take hitters who have faced 1 pitcher from a cluster, and see if he did in fact perform similarly against other pitchers in the cluster.
