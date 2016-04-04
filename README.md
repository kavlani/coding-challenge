Insight Data Engineering - Coding Challenge solution by Kamal Avlani
====================================================================

# Table of Contents
1. [Challenge Summary](README.md#challenge-summary)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Program and Package Version Details](README.md#program-and-package-version-details)
4. [Repo directory structure](README.md#repo-directory-structure)
5. [Testing directory structure and output format](README.md#testing-directory-structure-and-output-format)

## Challenge Summary
[Back to Table of Contents](README.md#table-of-contents)

This challenge requires the program to:

Calculate the average degree of a Twitter hashtag graph for the last 60 seconds, and update this each time a new 
tweet appears.  Hence this will be calculating the average degree over a 60-second sliding window.

A Twitter hashtag graph is a graph connecting all the hashtags that have been mentioned together in a single tweet.  

## Details of Implementation
[Back to Table of Contents](README.md#table-of-contents)

This program calculates the average degree of Twitter hashtag graph for the last 60 seconds.
As new tweets are processed, edges formed with tweets older than 60 seconds from the 
maximum timestamp being processed are evicted. 

This function reads from an input json file with Twitter data.
The hashtags and created_at fields from each tweet are extracted and stored in two arrays 
namely hashtags and time_stamps.

The program uses a pandas Series datastructure to store the time_stamps. However a 
list datastructure is used to store the hashtags essentially a list of sets structure,
since each tweet is a set of hashtags.
The pandas Series datastructure is used for its flexible and fast indexing capabilities 
relative to a list implementation. 

The underlying assumption is that even though the two array structures 
(namely time_stamps and hashtags) are independent, they are both of equal length.
Some additional logic has been implemented in the initial loading of arrays to ensure that
both are in sync and end up with the same number of elements by extracting hashtags only
where the created_at field is present in a JSON tweet. 
This also eliminates the rate limit messages from the json input file.

This program uses the networkx library for its speed and ease of use to create and 
maintain the Twitter hashtag graph in order to calculate the average degree.

Future Enhancements:

Future enhancements to the program could be to work on batch of tweets while parallelizing the processing of 
tweets since typically the file read operations have high latency. 

## Program and Package Version Details
[Back to Table of Contents](README.md#table-of-contents)

Following are the program/package version dependencies :

1. OS - Ubuntu 14.04.3
2. Python - Python 2.7.11 :: Anaconda 2.4.1 (x86_64)
3. Numpy - 1.10.1
4. NetworkX - 1.10
5. Pandas - 0.17.1
6. JSON - 2.0.9

All these packages are available with the Ananconda2 install. 
I have provided an install.sh script which installs Ananconda2, however requires accepting license manually. 
I am listing the path here also :

wget https://repo.continuum.io/archive/Anaconda2-2.4.1-Linux-x86_64.sh

## Repo directory structure
[Back to Table of Contents](README.md#table-of-contents)

The contents of `src` contains a single file called "average_degree.py".

Below is the output of the `tree` command:

├── insight_testsuite
│   ├── results.txt
│   ├── run_tests.sh
│   ├── temp
│   │   ├── run.sh
│   │   ├── src
│   │   │   ├── average_degree.py
│   │   │   └── __init__.py
│   │   ├── tweet_input
│   │   │   └── tweets.txt
│   │   └── tweet_output
│   │       └── output.txt
│   └── tests
│       ├── test-10k-tweets
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-1nodes-with-evict
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-2-tweets-all-distinct
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-empty-file
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-evict-tweet
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-malformed-tweets
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-mixed-dates
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-mixed-skip-evict-tweets
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-no-input-file
│       │   ├── tweet_input
│       │   └── tweet_output
│       │       └── output.txt
│       ├── test-outside60sec-tweet
│       │   ├── tweet_input
│       │   │   └── tweets.txt
│       │   └── tweet_output
│       │       └── output.txt
│       └── test-within60sec-tweets
│           ├── tweet_input
│           │   └── tweets.txt
│           └── tweet_output
│               └── output.txt
├── install.sh
├── README.md
├── run.sh
├── src
│   ├── average_degree.py
│   └── __init__.py
├── tweet_input
│   └── tweets.txt
└── tweet_output
    └── output.txt

42 directories, 35 files
## Testing directory structure and output format
[Back to Table of Contents](README.md#table-of-contents)

The run_tests.sh script was successfully run and passed.

