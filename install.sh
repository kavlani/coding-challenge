#!/usr/bin/env bash

# script to install anaconda2 package

# get the install script
wget https://repo.continuum.io/archive/Anaconda2-2.4.1-Linux-x86_64.sh

# start install in batch mode
bash -b Anaconda2-2.4.1-Linux-x86_64.sh -p $HOME/anaconda2

# setup path
export PATH=$HOME/anaconda2/bin:$PATH

