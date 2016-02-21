'''Version 0.2'''

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

#best performance by an actress in a motion picture - drama

import pickle
import json
import os.path

from awards_parse import *



def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts ={}
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    if (year == '2013'):
        with open('dbstore13.data') as infile:
                db = pickle.load(infile)
    else:
        with open('dbstore15.data') as infile:
                db = pickle.load(infile)

    ret_l = p_most_common(db)
    print ret_l
    return ret_l

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = {}
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners ={}
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters ={}
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    
    print "Beginning ceremony processing"

    # Sort and dump python list objects as text files
    if not os.path.exists('dbstore13.data') or os.path.exists('dbstore15.data'):
        with open('gg2013.json') as data_2013:
            db2013 = json.load(data_2013)
            data_2013.close()
            db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                                 for tweet in db2013
                                 if not check_retweet(tweet['text'])], key=lambda x:x[1])
                              #   and check_best(tweet['text'])], key=lambda x:x[1])
        with open('dbstore13.data', 'w') as outfile:
            pickle.dump(db_sorted, outfile)
        with open('gg2015.json') as data_2015:
            db2015 = json.load(data_2015)
            data_2015.close()
            db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                                 for tweet in db2015
                                 if not check_retweet(tweet['text'])], key=lambda x:x[1])
                              #   and check_best(tweet['text'])], key=lambda x:x[1])
        with open('dbstore15.data', 'w') as outfile:
            pickle.dump(db_sorted, outfile)
    print "Pre-ceremony processing complete."
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return

if __name__ == '__main__':
    main()
