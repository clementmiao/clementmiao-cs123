# Project Proposal
### By Charlie Fisher, Clement Miao, Sam Przezdziecki
=================
### Dataset
We are using Pitchf/x data, a pitch tracking system that tracks the velocity, movement, release point, spin, and pitch location for every pitch thrown in baseball, allowing pitches and pitchers to be analyzed and compared at a detailed level. We might also use Hitf/x, which is the equivalent for hits.  
We will be able to download this dataset using an R package, called "pitchRx", as explained in [this article](http://cpsievert.wordpress.com/2013/01/10/easily-obtain-mlb-pitchfx-data-using-r/), and save it as a collection of csv files. 

### Data Exploration & ideal outcome
After getting the data, we will agreggate all of the pitches that each pitcher threw, and then perform a clustering analysis on different aspects of their pitching style: pitch type, velocity, pitch break, etc. From this, we will be able to group similar pitchers together, and determine how similar they are to one another. Once we have this, we can take hitters who have faced 1 pitcher from a cluster, and see if he did in fact perform similarly against other pitchers in the cluster.

Hypothesis: Pitch type matters a lot more than other factors such as delivery type, etc. 

ideal outcome: If our clustering analysis works out, we should be able to have clearly defined clusters, and be able to make predictions about hitter performance given performance against other pitchers in the clusters. 

#### Tools
1. Hadoop : first task is to aggregate each pitch to a pitcher, so that a pitcher will be the key in a key-value pair, with the value being a vector of quantitative attributes of that pitcher. Second task would be running the k-means clustering on Hadoop. 

2. Mahout : We might use Mahout to run the k-means clustering, but it would be more interesting and educational to implement our own version of the k-means algorithm on Hadoop. 

#### Techniques
1. k-means clustering: Cluster by pitcher type (using aspects described above). We will translate the qualitative characteristics into quantitative metrics. 

2. Map-Reduce

3. Network: We might use a graph/network as our tool for both visualization and recommendation. After having determined the types of pitchers from our clustering, we will be able to translate those into a graph, from which we will be able to recommend a type of pitcher given a certain matchup against a hitter, and vice versa. 

### Desired Final Results & Implementation

In the end, we think there will be several clear clusters of pitchers, and hopefully find that batters fair similarly against pitchers within a given cluster. It is possible we may find that certain clusters do better overall, which might predict the future success of a new pitcher based on their attributes. 

Our implementation will hopefully be a recommendation tool for coaches, to help them determine who to put on the field from their benches for a given matchup. As a result, we will need a relatively quick recommendation time. 
