
########################################################################
### 
### Awards Parsing
###
########################################################################
#import nltk
import re
#from nltk.corpus import words
import difflib
### local
from events import *
from word_vector import *
import itertools
#### TMP
import json
db2013 = {}


import pickle
import os.path


def check_retweet(string):
    if string.find("RT ") != -1:
        return True
    return False


def check_best(string):
    if string.find("Best") != -1:
        return True
    return False

def dump_obj():
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

#if not os.path.exists('dbstore13.data') or os.path.exists('dbstore15.data'):
 #   dump_obj()

#with open('dbstore13.data') as infile:
 #   db2013 = pickle.load(infile)
    
#with open('dbstore15.data') as infile:
 #   db2015 = pickle.load(infile)



#    db2015 = sorted(db2015, key=lambda x: (int(x['timestamp_ms'])), reverse=False)
 
EVENTS_AWARDS = []

#keys = {'timestamp_ms', 'text'}
#db2015_n = {key:db2015[key] for key in keys}

#newdict = {}
#for tweet in db2015:
 #   for f in fields:
        

#newdict = {}
#for tweet in db2015:
 #   newdict[tweet['text']] = int(tweet['timestamp_ms'])
#newdict = sorted(newdict)



 
    




#### Awards Parsing ####

        
def check_integrity(string):
    ## Currently not using this-> massive peformance decrease
    '''Returns false if string contains spelling errors'''
    for token in string.split():
        if token not in words.words(): return False
    return True


def count_tokens(string):
    count = 0
    for char in string:
        if char.isspace(): count+=1
    return count


def get_awards_matches(db, i, num_tweets):
    '''[JSON DB] db, [U_Int] i, [U_Int] num_tweets -> List-of Matches'''
    MIN_MATCH_THRESHOLD = 30
    MIN_EVENTS_MATCH_THRESHOLD = 40
    WORD_GRAB_COUNT = 10
    def find_and_cut_or_add(matches_vec, string, start_i):
        # Cut the award if already in list, otherwise add it
        if count_tokens(string) <= 2: return
        for award in EVENTS_AWARDS:
            ind = 0
            for n in range(0, len(string)):
                ind +=1
                if (n >= (len(award)-1)): break
                if (string[n] != award[n]): break
      #      if (ind > MIN_EVENTS_MATCH_THRESHOLD):  #Skip if not really a match
       #         award[1] += 1
        #        return  #if we find it was the award for a previous event, dont include it
            print award[0], string
            if difflib.SequenceMatcher(None, award[0], string).ratio() >= .6:
                if len(award[0]) >= len(string):
                    award[1] += 1
                    return
                else:
                    award[0] = string
                    award[1] += 1
                    return
        for match in matches_vec:
            ind = 0
            for n in range(0, len(string)):
                ind +=1
                if (n >= (len(match[0])-1)): break
                if (string[n] != match[0][n]): break
            if difflib.SequenceMatcher(None, match[0], string).ratio() <= 0.75: continue
       #     if (ind < MIN_MATCH_THRESHOLD): continue #Skip if not really a match
            else:
              #  if (match[1] <=4 ): match[0] = match[0][:ind] #only alter entry if singleton
                match[1] += 1
                return
        matches.append([results_str, 1]) #if no match append
    def trim_award(string):
        # Trim a string before colon
        ret_str = ""
        for n in range(0, len(string)):
            if (not string[n].isalpha() and not string[n].isspace()):   # == ":" or string[n] == "-"
                if (string[n] != ","):
                    return ret_str
            ret_str += string[n]
        return ret_str
    event_i = get_event_indicies(get_tpm_arr((db)))[i]
    matches = []
    for n in range(0,num_tweets):
        results_str = "Best "
        tweet_i = event_i + n
        tweet = ""
        tweet = db[tweet_i][0]
        find_i = tweet.find("Best")
      #  find_i = re.search("best", tweet, re.IGNORECASE) #
       # if (not find_i): continue
        # find_i = find_i.start()
        start_i = find_i 
        if (find_i == -1): continue
        tweet_index_vec = get_string_indicies(tweet)
        tweet_index_vec_len = get_len(tweet_index_vec)
        find_i = find_ind(find_i, tweet_index_vec)
        for j in range(0,WORD_GRAB_COUNT):
            find_i += 1
            if (find_i >= tweet_index_vec_len):
                break
            word = get_word(find_i, tweet_index_vec, tweet)
            if(word[:1].islower() and not (word == "in" or word == "a")):
                break
            else:
                tmp_word = word.lower()
                if (tmp_word == "television"):
                    results_str += "TV "
                elif (tmp_word == "film" or tmp_word == "movie"):
                    results_str += "Motion Picture "
                elif (word == "in"):
                    results_str += ", "
                elif (word == "a"): continue
                elif (tmp_word == "feature"): continue
                else:
                    results_str += word + " "
        if (results_str != ""):
            results_str = trim_award(results_str)
            find_and_cut_or_add(matches, results_str, find_i)
    return matches


def most_common_match(db, i, num_tweets):
    ga = get_awards_matches(db,i,num_tweets)
    if ga == []:
        return False
    else:
        return sorted(ga, key=lambda x:x[1], reverse=True)[0] #:2

def remove_similar(vec):
    for awardA, awardB in itertools.combinations(vec, 2):
        if difflib.SequenceMatcher(None, awardA[0], awardB[0]).ratio() >= 0.90:
            awardB[1] += awardA[1]
            awardA[1] = 0
    return vec
        
def remove_similar2(vec):
    ittr = 1
    for award in vec:
       # ittr +=1
        l_award = len(award[0])
        for n in range(0,len(vec)):
            n_award = vec[n]
            if n_award == award : continue
            l_n_award = len(n_award[0])
            if(l_n_award < l_award): continue
            match_r = round(0.7*l_n_award) #amt that must match in order to be considered same
            ind = 0
            for i in range(0,l_award):
                if award[0][i] != n_award[0][i]:
                    break
                ind +=1
            if ind >= match_r:
                n_award[1] += award[1]
                award[1] = 0
                break

def collapse_adjacent(v_awards):
    return -1



def format_output(awards_l):

    p_awards_l = []
    for award in awards_l:
        curr_str = award
        act_ind = award.find("Act")
        sup_ind = award.find("Support")
        add_sup = False
        if sup_ind != -1:
                add_sup = True
        if act_ind != -1:
            ittr = 0 
            for n in range(14):
                if award[act_ind+n].isspace(): break
                ittr +=1
            if add_sup == True:
                curr_str = curr_str[:(act_ind+ittr)] +' in a Supporting Role ' + curr_str[act_ind+ittr:]
            curr_str = curr_str[:act_ind] +'Performance by an ' + curr_str[act_ind:]
            if add_sup == True:
                ittr=0
                for n in range(14):
                    if award[sup_ind+n].isspace(): break
                    ittr +=1
                curr_str = curr_str[:sup_ind] + curr_str[sup_ind+ittr+1:]
        p_awards_l.append(curr_str)
    return p_awards_l

def p_most_common(db):
    EVENTS_AWARDS = []
    EVENTS = get_event_indicies(get_tpm_arr(db))
    NUM_EVENTS = len(EVENTS)
    stripped_vec = []
    for n in range(0,NUM_EVENTS-1):
        most_common = most_common_match(db, n, 1300)
        if most_common: EVENTS_AWARDS.append(most_common)
    remove_similar(EVENTS_AWARDS)
    for award in EVENTS_AWARDS:
        c_string = award[0].split()
        c_string[len(c_string)-1]
        if award[1] > 10 and c_string[len(c_string)-1][0].isupper(): #ensure ending on caps
#            print award
            stripped_vec.append(award[0])
    return format_output(stripped_vec)
