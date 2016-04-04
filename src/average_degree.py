
# coding: utf-8

import os
import sys
import json
import pandas as pd
import datetime as dt
from datetime import timedelta
import networkx as nx
import itertools as it
import numpy as np
import dateutil as du

window_size = 60  # Defines the window_size in seconds
parse_date = du.parser.parse
get_combinations = it.combinations


def get_htags(tweet):
    """
 This function processes each tweet to extract the set of DISTINCT hashtags in each tweet.
 The input parameter is a tweet which is :
   a list of dicts with 'text' as a key in the dict 

 Only the 'text' field is extracted and put into a set to get a unique list of hashtags.
 
 This function returns :
   a set of hashtags
 
    """
    hash_set = set()                    # Initialize set
    for htag in tweet:
        if 'text' in htag:              # Check if 'text' field is present
            hash_set.add(htag['text'])  # Add each hashtag to the set
    return hash_set


def avg_degree(time_stamps, hashtags):
    """ 
 This function calculates the average degree of Twitter hashtag graph for the last 60 seconds, 
 and updates this each time a new tweet appears. 
 Hence it calculates the average degree over a 60-second sliding window.
 A Twitter hashtag graph is a graph connecting all the DISTINCT hashtags that 
 have been mentioned together in a single tweet.

 As new tweets are processed, edges formed with tweets older than 60 seconds from the 
 maximum timestamp being processed are evicted. 
  
 This function uses the networkx library for its speed and ease of use to create and 
 maintain the Twitter hashtag graph in order to calculate the average degree.
 
 The input parameters for this function is :
    a pandas series for time_stamps
    a list of hashtags
 
    """
    n = len(time_stamps)            # Length of tweet data to process
    cur_row = 0                     # Index to access timestamp and hashtag arrays

    tag_graph = nx.Graph()          # Create a graph using networkx module
    mean_degree = 0.                # Initialize mean_degree output variable

    donot_include = set()           # Initialize donot include list to track timestamps 
                                    # already filtered for eviction of edges
    
    if len(time_stamps) and len(hashtags): # Check to make sure hashtags and time_stamps have some values
        window_start = time_stamps[0]      # Current Window start timestamp
        cur_end = time_stamps[0]           # Current Window end timestamp init to same as start
    else:
        print('%.2f' % 0.)
        return
    
    while cur_row < n:              # Continue processing till all lines processed
        
        # Initialize variables for every loop
        
        tag_list = []                # Tag list to create/evict edge combinations for graph
        edge_list = []               # Edge list to add/evict edge(s) to the graph
        
        # Only update next window start time if new timestamp is higher than current window_start
        if time_stamps[cur_row] > window_start:          
            window_start = time_stamps[cur_row]
        
        # Process timestamps for adding/evicting edges in the graph
        # also update window_end with possibly new window_start
        window_end = window_start - timedelta(seconds=window_size)


        # Check to see if current timestamp is outside of 60-sec window
        # Update current window end marker and evict previous edge(s)
        # Process evict before insert of current edge to account for current edge which might be a
        # duplicate of existing edge in the graph so will be evicted but if insert is processed first then
        # the new edge will not be added
        if cur_end < window_end:
            cur_end = window_end
        
           # Get indices for timestamps older than 60 sec - to access hashtag array (use set for perf.)
            time_index = set(time_stamps[time_stamps < window_end].index)
            
            filter_index = time_index.difference(donot_include) # filter index to only include
                                                                # indices which were not skipped
            donot_include |= filter_index                       # Set union - add already processed indices to
                                                                # do not include list
            
            for idx in filter_index:                        # Need to iterate over all indices
                if idx < cur_row:                           # Only process "older" rows than
                    tag_list = hashtags[idx]                # current
                    
                    if len(tag_list) > 1:                 # Only evict tags for > 1 node
                        edge_list = list(get_combinations(tag_list,2))
                        tag_graph.remove_edges_from(edge_list)  # Remove edge(s) from graph
            
            to_prune = nx.isolates(tag_graph)             # Prune for isolated nodes
            tag_graph.remove_nodes_from(to_prune)         # after edge removal


        if (time_stamps[cur_row] >= window_end):
            tag_list = hashtags[cur_row]  # Get the hastag list for current row if the current
                                         # timestamp is within the window else
                                         # include the current index in the do not include set
                                         # since the graph should not remove this edge
                        
            if len(tag_list) > 1:                                # Add edges for > 1 node only
                edge_list = list(get_combinations(tag_list,2))   # Get edge combinations
                tag_graph.add_edges_from(edge_list)             # Add edges to the graph
        else:
            donot_include.add(cur_row)                          # Add skipped timestamp index 
                                                                # to the donot_include list
                                                                # which will be used during eviction
        degree_values = nx.degree(tag_graph).values()
        
        if len(degree_values):
            mean_degree = np.mean(degree_values)          # Use np mean for perf.
        else:
            mean_degree = 0.

        print ('%.2f' % mean_degree)

        cur_row += 1                                     # Advance to process next tweet


def main():
    """
 This function reads from an input json file with Twitter data.
 The hashtags and created_at fields from each tweet are extracted and stored in two arrays 
 namely hashtags and time_stamps.
 
 The function uses a pandas Series datastructure to store the time_stamps. However a 
 list datastructure is used to store the hashtags essentially a list of lists structure.
 The pandas Series datastructure is used for its flexible and fast indexing capabilities 
 relative to a list implementation. 

 The underlying assumption is that even though the two array structures 
 (namely time_stamps and hashtags) are independent, they are both of equal length.
 Some additional logic has been implemented in the initial loading of arrays to ensure that
 both are in sync and end up with the same number of elements by extracting hashtags only
 where the created_at field is present. This also eliminates the rate limit messages from
 the json input file.

    """

    try:
        file_path = sys.argv[1]                      # Check if no input file given
    except Exception:
        print('Please input file path with filename')
        sys.exit()
        
    if not os.path.isfile(file_path):                # Check if input file/path is wrong and exit
        print('Input file does not exist')
        sys.exit()

    records = [json.loads(line) for line in open(file_path)]  # Load json file into records array
    
    time_str = pd.Series([rec['created_at'] for rec in records if 'created_at' in rec])
    
                                                      # Extract tweets - list of 'text' hashtags
    tweets = [rec['entities'].get('hashtags', []) if ('entities' in rec) else [] \
              for rec in records if 'created_at' in rec]

    del records                                       # Delete records to free up memory

    time_stamps = time_str.apply(parse_date)          # Convert date strings to time_stamps

    del time_str                                      # Delete time_str array to free up memory

    hashtags = map(lambda x: get_htags(x), tweets)    # Get set of distinct hashtags from each tweet

    del tweets                                        # Delete tweets array to free up memory
    
    if len(time_stamps) and len(hashtags):            # Only process if there are some time-stamps
        avg_degree(time_stamps, hashtags)
    else:
        print ('%.2f' % 0.)

if __name__ == '__main__':
    main()

