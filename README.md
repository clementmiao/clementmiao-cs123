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

3. Neo4j: graph database potentially for our recommendation tool. 

#### Techniques
1. k-means clustering: Cluster by pitcher type (using aspects described above). We will translate the qualitative characteristics into quantitative metrics. 

2. Map-Reduce

3. Network: We might use a graph/network as our tool for both visualization and recommendation. After having determined the types of pitchers from our clustering, we will be able to translate those into a graph, from which we will be able to recommend a type of pitcher given a certain matchup against a hitter, and vice versa. 

### Desired Final Results & Implementation

In the end, we think there will be several clear clusters of pitchers, and hopefully find that batters fair similarly against pitchers within a given cluster. It is possible we may find that certain clusters do better overall, which might predict the future success of a new pitcher based on their attributes. 

Our implementation will hopefully be a recommendation tool for coaches, to help them determine who to put on the field from their benches for a given matchup. As a result, we will need a relatively quick recommendation time. 

#Project Prototype
### May 5th Update
==================
### Process to run the prototype
- For Charlie
- To convert to json: 
    pip install https://github.com/hay/xml2json/zipball/master
    cd /usr/local/bin
    chmod +x xml2json
     

### Dataset
folder: [june_data](https://github.com/clementmiao/clementmiao-cs123/tree/master/june_data)

file: [xml2jsonScript.py](https://github.com/clementmiao/clementmiao-cs123/blob/master/xml2jsonScript.py)

The data set is from the pitchf/x database from the MLB Advanced Media Department. To get the data, we used a perl script from [this website](http://codepaste.net/ppw1oo) by Mike Fast. For our prototype, we are taking one month's worth of pitches(about 80,000 total) and agragating them by pitcher and pitch type. One of the challenges was to convert all of the xml files that are returned from the MLBAM website into json files that are easier to work with. 

### Aggregation
file: [aggregate.py](https://github.com/clementmiao/clementmiao-cs123/blob/master/aggregate.py)

We now have a folder of JSON files. We created a python script that takes in a folder, and creates a dictionary of pitchers, with key-value pairs for each pitcher being: total pitches thrown, handedness (left or right handed), and dictionaries of pitch type attributes. For the latter, say that we are looking at the sub dictionary of "FF" (Four Seams FastBall), the key will be "FF", with values being sums of break_angle (the angle formed by the verticle line that passes through where the pitch would have ended up if it had traveled perfectly straight from the pitcher's hand and the line through where it actually crossed home plate), break_length (distance between where it would have been if it had been straight from pitchers hand and where it ended up), break_y (how far in front of home plate did the pitch start breaking), pfx_x, (the distance measure of horizontal movement) pfx_z (distance measure of vertical movement), spin_dir (which way the ball was spinning), spin_rate (how fast the ball spins), start_speed (how fast the ball leaves the pitcher's hand), x0, y0, z0 (the x,y,z coordinates of the release point of the pitcher). We decided to aggregate these attributes by pitch type because we believe that a pitcher's fastball and curveball have very different speeds for example, so it would make little sense to average the speed of a fastball and a curveball, and rather should average the speed of all curveballs by that pitcher. 

Subsequently, we average all these attributes per pitch type per player, and return a list of tuples, with tuple[0] being the player id, and tuple[1] being a dictionary of attributes of the player. 

Since the data is relatively messy and at times does not follow its own pattern, a number of conditionals were needed to parse through the labyrinthine data. 

Running all this for one month's worth of data returns our desired list of players in around 15.1s, which means a full 6 years worth of data will take us around 10 minutes, considering constant overhead. With parallelization, we could cut this time down even further, and account for the possibility of larger data sets in the future. 

### Clustering
file: [clustering.py](https://github.com/clementmiao/clementmiao-cs123/blob/master/clustering.py)

We have implemented a k nearest neighbors algorithm for determining the k pitchers most similar to any given pitcher, contained in the prototype database. We believe the algorithm yields reasonable results -- that is, it returns pitchers who have similar repertoires. Nonetheless, we would still like to explore ways to polish and remove unhelpful parameters from the 
dataset.

Looking forward, we will implement other clustering algorithms, and analyze their effectiveness. We have made some efforts to implement a k means clustering algorithm, but have some doubts that the pitcher data fits neatly in clusters, which may be causing problems with this technique.


### Remaining Tasks
- Matchups: We need to go through each hitter and find how they did aginst different clusters that we determine from our analysis. Since all of the data is organized by at-bats, aggragating a single hitter's at-bats could be more computationally expensive and might require parallelization.
- Parallelization: The Aggregation task can be converted into a map-reduce task, whereas the clustering could also be performed in a similar fashion. Additionally, the matchups could be parallelized using MPI.
- Recommendation engine: Given our data, and if we implement the matchups part correctly, putting the data inside a graph database will allow for fast traversals hence fast recommendation for coaches.
- Visualization: If enough time, we would like to be able to visualize the clusters.


###Challenges ahead
With our current project, we believe that the benefits of parallelization are not fully maximized, as they would be more significant if we had a larger data set, or if we had more computationally expensive algorithms/analysis. Since we won't have a larger data set as we are grabbing the whole data set already, to fully realize the educational benefits of implementing parallelization, we are looking into performing more complex operations than pure clustering, even though we are running through multiple clustering methods. 
Some of our ideas:
- Making our recomendation smart enough to potentially predict the other manager's move. For example, if our engine said to use hitter A, the opposing team might then swithch with pitcher B, which may be a worse matchup than the original. We can try to have our recommendation engine predict this switch, and adjust its recommendation accordingly through a game theoretical approach.
- Performing Time-Series Analyses of players, either over a game or across the past few years.

### Task Division
We will divide the tasks into the following groups, with the goal of completing each of these by 8th week:
- One member will handle parallelizing the current code, including aggregation and clustering.
- The other two will work on the recommendation and visualization, as well as implementing one of the additional ideas.