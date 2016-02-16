
########################################################################
### 
### Awards Parsing
###
########################################################################
import nltk
import re
from nltk.corpus import words

### local
from events import *
from constants import *
from word_vector import *

EVENTS = get_event_indicies(get_tpm_arr(db2013))
NUM_EVENTS = len(EVENTS)
EVENTS_AWARDS = []

#### Awards Parsing ####
def check_integrity(string):
    ## Currently not using this-> massive peformance decrease
    '''Returns false if string contains spelling errors'''
    for token in string.split():
        if token not in words.words(): return False
    return True


def get_awards_matches(db, i, num_tweets):
    '''[JSON DB] db, [U_Int] i, [U_Int] num_tweets -> List-of Matches'''
    MIN_MATCH_THRESHOLD = 30
    WORD_GRAB_COUNT = 10
    def find_and_cut_or_add(matches_vec, string, start_i):
        # Cut the award if already in list, otherwise add it
        for award in EVENTS_AWARDS:
            ind = 0
            for n in range(0, len(string)):
                ind +=1
                if (n >= (len(award)-1)): break
                if (string[n] != award[n]): break
            if (ind < MIN_MATCH_THRESHOLD): continue #Skip if not really a match
            else:
                return #if we find it was the award for a previous event, dont include it
        for match in matches_vec:
            ind = 0
            for n in range(0, len(string)):
                ind +=1
                if (n >= (len(match[0])-1)): break
                if (string[n] != match[0][n]): break
            if (ind < MIN_MATCH_THRESHOLD): continue #Skip if not really a match
            else:
                if (match[1] <=4 ): match[0] = match[0][:ind] #only alter entry if singleton
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
        tweet = db[tweet_i]['text']
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
                results_str += word + " "
        if (results_str != ""):
            results_str = trim_award(results_str)
            find_and_cut_or_add(matches, results_str, find_i)
    return matches

def most_common_match(db, i, num_tweets):
    return sorted(get_awards_matches(db,i,num_tweets), key=lambda x:x[1], reverse=True)[1] #:2

def p_most_common():
    for n in range(0,NUM_EVENTS-1):
        EVENTS_AWARDS.append(most_common_match(db2013, n, 1300))
    for award in EVENTS_AWARDS:
        print award[0]
