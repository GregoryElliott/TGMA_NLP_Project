
########################################################################
### 
### Awards Parsing
###
########################################################################
import nltk
import re
from nltk.corpus import words
import difflib
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


def count_tokens(string):
    count = 0
    for char in string:
        if char.isspace(): count+=1
    return count

def get_awards_matches(db, i, num_tweets):
    '''[JSON DB] db, [U_Int] i, [U_Int] num_tweets -> List-of Matches'''
    MIN_MATCH_THRESHOLD = 30
    MIN_EVENTS_MATCH_THRESHOLD = 20
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
            if (ind > MIN_EVENTS_MATCH_THRESHOLD):  #Skip if not really a match
                award[1] += 1
                return #if we find it was the award for a previous event, dont include it
            if difflib.SequenceMatcher(None, award[0], string).ratio() >= 0.85:
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
            if difflib.SequenceMatcher(None, match[0], string).ratio() <= 0.6: continue
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
    ga = get_awards_matches(db,i,num_tweets)
    if ga == []:
        return False
    else:
        return sorted(ga, key=lambda x:x[1], reverse=True)[0] #:2


def remove_similar(vec):
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

def remove_similar_B(vec):
    ittr = 1
    for award in vec:
        ittr +=1
        for n in range(ittr,len(vec)):
            n_award = vec[n]
            if n_award[1] == 0: continue
            if(len(n_award) < len(award)): continue 
            if difflib.SequenceMatcher(None, award[0], n_award[0]).ratio() >= 0.60:
                n_award[1] += award[1]
                award[1] = 0
                
def p_most_common():
    for n in range(0,NUM_EVENTS-1):
        most_common = most_common_match(db2013, n, 1300)
        if most_common: EVENTS_AWARDS.append(most_common)
    remove_similar(EVENTS_AWARDS)
    for award in EVENTS_AWARDS:
        c_string = award[0].split()
        c_string[len(c_string)-1]
        if award[1] > 20 and c_string[len(c_string)-1][0].isupper(): #ensure ending on caps
            print award
