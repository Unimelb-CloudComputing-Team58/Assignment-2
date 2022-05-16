#!/bin/bash

###################################################
#  University of Melbourne                        #
#  COMP90024 Cluster and Cloud Computing          #
#  2022 Semester 1 - Assignment 2                 #
#                                                 #
#  Team 58:                                       #
#  - (Sam)     Bin Zhang     895427  @ Melbourne  #
#  - (Joe)     Tianhuan Lu   894310  @ Melbourne  #
#  - (Leo)     Yicong Li    1307323  @ Melbourne  #
#  - (Peter)   Weiran Zou   1309198  @ Melbourne  #
#  - (Thomas)  Chenhao Gu   1147534  @ Melbourne  #
###################################################

. ./openrc.sh; ansible-playbook --ask-become-pass pb-main.yaml