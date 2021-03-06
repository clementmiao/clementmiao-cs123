#For Project Report, See below (Cmd+F Project Report)
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
- To get the data, run the mlbscript.pl perl file. Currently, the file is set to download the enire 2011 season. To download a specific time interval:
    Change the start time in line 56: 

        $start = timelocal(0,0,0,31,2,111);

    starts from March (months are indexed from zero, so Jan = 0, Dec = 11) 31st, 2011 (111 years after 1900). To get data from Just june for example, the code would be $start = timelocal(0,0,0,1,5,111);
    Simillarly, change the end time in line 63: 

        $now = timelocal(0,0,0,31,9,111)

    To get it to stop at June 30th, 2011, the code would be $now = timelocal(0,0,0,30,5,111);
    Next, run the following code to get the data:

        perl mlbscript.pl


- To convert to json: 

        pip install https://github.com/hay/xml2json/zipball/master
        cd /usr/local/bin
        chmod +x xml2json
        mkdir june_data
        python xml2jsonScript.py

- To aggregate the json files into a pickle file of a list of player tuples:

        python aggregate.py 

- To run a test case of a k-nearest neighbors clustering on Max Scherzer:
        
        python clustering.py


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

#Project Report 
==================
## Process to run the project
###
=======

Local Machine:
- Get the data using the perl script as before, modifying the required lines to get the desired range:

        perl get_data.pl
- Run:
 
        movefiles.py
to get all of the games into one folder to work with hadoop.
- Run:
 
        movefiles_players.py 
to create a folder of all the players.xml into one players folder.
- Run:
 
        nohup scp -r flat_games_all midway.rcc.uchicago.edu:/tmp/clement 
to put it into midway hadoop.

Midway Cluster (run: ssh midway.rcc.uchicago.edu):
- Run:
 
        hdfs dfs -copyFromLocal /tmp/clement/flat_games_all input_aggregation 
, to put the data in hdfs.
- Run:
 
        sh run_aggregation.sh [input_folder] [output_folder] [RES_FILE]
to run the hadoop job. The shell script will put a file [input_folder] into the midway-hadoop filesystem, output to [output_folder] on hdfs, and then does a getmerge to put the file [RES_FILE] in the local directory on midway. 
- Run:
        git add [RES_FILE]
This is the RES_FILE from the previous step
- Run:

        git commit -m"passing results"
- Run:

        git push origin master
        
Back on the local machine ( we do this because numpy is not loaded in midway hadoop):
- Run:

        git pull
- Run:
 
        python k_means.py [k] [input_file] [output_file] 
, replacing "k" with the number of clusters desired. The input_file is the file that should have just been git pulled. In our case, "input_file" was results_aggregation.txt" and "output_file" was "clusters.txt".
- Run:

        git add [output_file]
Where the output file is the output_file from the previous step.

- Run:

        git commit -m"[Message here]"
        
- Run:

        git push origin master
        
On Midway-Hadoop machine (ssh midway.rcc.uchicago.edu):
- Run:
        git pull 
To get the clusters file from the previous steps.
- Run: 
        cp cluster_file clusters.txt
- Run:
        hdfs dfs -rm clusters.txt
Do this step if clusters.txt is already on hdfs.
- Run:
 
        hdfs dfs -copyFromLocal clusters.txt
This will put the file clusters.txt in our case into hdfs (unfortunately it has to be named clusters.txt because of our hadoop code). 
- Run:
 
        sh run_matchup.sh
to run the matchups on hadoop.

This will give you one set of data. Once you have 2 sets of data, you can use one as the training set and one as the testing set by running the command:

        python accuracy_test.py [training data] [testing data]
This will return the "score" (which is basically average OBP difference) between the two sets of data. 

- Run:
 
        neo4j start
to start the neo4j server
- Run:
 
        python graph_db.py main
to add the results into our Neo4j database

- Run: 

        python graph_db.py hitter [pitcher_name] [your_team]
to recommend a hitter for your team
    or:

        python graph_db.py pitcher [hitter_name] [your_team]
to recommend a pitcher for your team. Ex:

        python graph_db.py pitcher "Ichiro Suzuki" "New York Yankees"

## The Process Broken down
### Aggregation
Our approach for aggregating pitchers is the same as before. This time, we parallelized the process using hadoop. Each mapper is given a game, and then determines the pitch type and adds the desired attributes to that pitch. The combiner and reducer take that list (whch also has how many times each pitch type was thrown), and then averages the attributes for each pitch for that pitcher.
    The challenges for this one are that first of all, our prototype had done it in a way that was not parallelized. Our original implementation depended on a python dictionary that held all the data, hence a challenge for this process was writing an implementation of Writable that could hold the data for each pitcher. Secondly, our original implementation in the prototype first converted the game files to JSON, however in the Hadoop implementation, we decided to skip a step and manipulate XML files directly, using a reader object that goes through each XML tag. 
At the end of the process, we output a txt file for which each line has the following format:
player_id, total_pitches, left_handed (1 if true, 0 else), right_handed (1 if true, 0 else), {the 11 averages of attributes for FF and a counter for FF thrown}, {the 11 averages of attributes for FT and a counter for FT thrown}, etc for the other 9 types of pitches thrown. 
For some players, you might notice that their entire arrays is filled with 0s (except for their handedness), as the pitch f/x has some holes in it, especially in the earlier years, when a lot of the data we need for our analysis and aggregation processes were not recorded. We have written our code to take into account those cases.
###Clustering
This process takes the end result file of the aggregation process, and an integer k as number of clusters, dividing the pitchers from the input file into lists of pitcher clusters. 
We cluster them with a k-means algorithm. 
For the initial placement of the centroids, we decided to use an algorithm called k-means++, because it guarantees that the final clustering will be reasonably close to the optimal clustering. The first centroid is chosen randomly from the points. Then we calculate D(x) for each point x, the distance to the nearest centroid. To choose the next centroid, we select from the remaining points with choice weighted by D(x)^2.
After the initial seeding, we proceed to do a standard k-means clustering. We assign each point to the nearest centroid, then recalculate the centroids by averaging all of the points within the cluster.


###Matchups
Our file goes takes in a list of clusters that was output from the previous step and goes through each game and keeps track of how each batter did against the different clusters, and outputs a text file where each line is a batter with one pair of (hits + walks, plate appearences) for each cluster.
    Once again, we used Hadoop to do this task, and one of the difficulties we faces was being able to have hadoop read in both the clusters text file and the game data to work with while still having both sets of information accessible to all mappers. Hence somehow, we needed to "parallelize" the clusters file, and purely loading it onto hdfs and reading it that way did not initially work. What ended up working was caching it on hdfs, havving in the setup function of the mapper that would be able to read this file from the hdfs cache, and then population an ArrayList of strings, which each element of the ArrayList representing a series of pitchers who belong in the same cluster. 

###Graph Database
For efficient recommendation, we combine 3 sources of tabular data -- player info, cluster info, and matchups -- into a graph database. The player info contains the MLBAM player id, the player's full name, and the players current team. The cluster info contains the pitcher's MLBAM player id and which cluster he has been assigned to. The matchups contain each player's MLBAM player id, his total plate appearances over the date arrange, and for each cluster, his total number of walks and hits and his total number of plate appearances.

To create the graph database, we used the python library py2neo to access neo4j through the REST api. We also made use of neo4j's web interface. We have nodes representing teams, clusters, and players (including both pitchers and batters). We make no type distinction between pitchers and batters, because almost all pitchers are batters as well at times. Between players and clusters, we have the relation 'BELONGS TO,' representing that a pitcher belongs to a cluster. We also have the relation 'MATCHUP' which represents how well a batter did against a cluster and contains the properties OBP (on-base percentage) and PA (plate appearances). Between players and teams, we have the relation 'PLAYS FOR'. 

This structure facilitated easy access to the information we wanted using CYPHER to query the database. We provide recommendations for batters to face specific pitchers in a few seconds at most, and much of this time is spent connecting to the server.


###Testing Our Results
To test our results, we take a large sample of our data, find out what there expected on base percentage would be against a given cluster, and then see haow he actually did against those clusters in another set of our data. To gauge accuracy, we sum up the differences in OBP between our testing and training data sets, weighted by how many plate appearences are in our testing set (that way, predicting 20-40 when it is actually 0-40 is worse than predicting 1-2 when it is actually 0-2) Summing up all of these differences gives us a "score" for the fit, where lower is better. We then divide by the total number of plate appearences to give us approximately what the average difference between the predicted and actual values are. The score will range from 0 (where every prediction is pefect) to 1 (where an out is predicted every time and in actuallity there are no outs, or vice versa). We can compare our clusters to a random clustering to see how our score compares. To generate random clusters, add 'random' as another command line argument to the k-means cluster function

## Design
Our current implementation is just a series of command line commands to go from data acquisition from the MLB website to a working graph database. The current user interface is the web interface of Neo4j, and a certain Cypher command can give you a ranked list of players who you should put on the field, given the opposite team. 
With such an interface, we can test a few scenarios easily, through the py2neo library, and hence take advantage of python's useability.
Of course, this is not yet a tool which a coach can use live on the baseball field during a game. A quick tool that would make it a lot easier for a coach would be a small python script that given two command line arguments of a opposing player and a team, would translate that into a copy-pasteable cypher command, to put in the web interface. Of course, in this case a low-tech solution works very well, in which the coach before a game could just print out the recommended players for all possible opposing players during the coming game, to easily make a quick decision.

## Reflections on tools 
### Java
We mostly used Java to work with Hadoop. Type-checking was often useful during the process of writing Hadoop mappers and reducers, as the manipulation of data got confusing at times.

### Python
We mostly used Python for quick scripts, to process data, to create the clusterings, as well as loading data into Neo4j. Python was a useful glue programming language, for when we needed a small task done, or for when dictionaries proved especially useful. We mostly used Python during the prototype phase, as the flexibility was really advantageous, as well as the quick prototyping. However, the lack of static typing at times led to errors that went unnoticed, for example integer division happening instead of float division. 

### Hadoop
Hadoop is nice for what we wanted to do; It let us execute a relatively simple task on lots of files all at the same time. However, sometimes Hadoop lacked the flexibility to do some of the things that we wanted to do, such as read things from two different files. Initially, we thought that there would not be any speed benefits to using Hadoop, however, it seems like hadoop is indeed very useful for the matchups job (getting batters' OBP vs. clusters). Additionally, using our python script to run the aggregation process, we ran into the case where the dictionary that was loaded into memory was so big that it would freeze our computers. Hence, we see the benefits of parallelization.

### Git/Github
During this whole project, we have been using git and github as our workflow management tool. This has been useful, as we often were unable to meet face to face, hence it allowed us to work independently, while still having access to the others' progress.

### Neo4j and py2neo
Neo4j was very useful for creating our recommendation engine. As it was our first time using neo4j for intensive purposes, the web user interface was extremely helpful for checking and debugging. Being familiar with SQL, CYPHER was a comfortable adjustment. We definitely hope to incorporate graph databases into future work, as it is much nicer to work with than tabular data at times.


## Conclusion
After running our tests on both 2008 as our training data and 2009 as our test data, we get a score of .1165 when using our clustering method with 20 clusters, compared to a score of .1291 when using random clusters. This difference may not seem very big, however, if scores are thought of in terms of OBP differences, then when you consider that the standard deviation of OBP in the MLB is about .033, this suggests that our clustering predicts about a half standard deviation better than random. While we might have hoped for a slightly larger difference, we difinetly have evidence to support out idea that clustering pitchers does provide additional informathion than just using individual matchups. A further extension would be to try to do in season comparisons (i.e use 5 months of the season to predict the 6th), because even though there will be much smaller sample sizes, we eliminate the potential effects of being in different years. Furthermore, we need to do further analysis of the influence of k (number of clusters) on our results. We believe that by varying k, we might be able to determine the 'optimal' configuration. (We will have additional insights for the presentation as we tweak our inputs)

