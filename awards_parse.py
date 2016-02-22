
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

import nltk

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
                       #      if not check_retweet(tweet['text'])], key=lambda x:x[1])
                            if check_best(tweet['text'])], key=lambda x:x[1])
    with open('dbstore13.data', 'w') as outfile:
        pickle.dump(db_sorted, outfile)
    with open('gg2015.json') as data_2015:
        db2015 = json.load(data_2015)
        data_2015.close()
        db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                            for tweet in db2015
                        #    if not check_retweet(tweet['text']) and
                            if check_best(tweet['text'])], key=lambda x:x[1])
    with open('dbstore15.data', 'w') as outfile:
        pickle.dump(db_sorted, outfile)

def dump_obj2():
    with open('gg2013.json') as data_2013:
        db2013 = json.load(data_2013)
        data_2013.close()
        db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                            for tweet in db2013
                            if not check_retweet(tweet['text']) and
                            check_best(tweet['text'])], key=lambda x:x[1])
    with open('dbstore13.data', 'w') as outfile:
        pickle.dump(db_sorted, outfile)
    with open('gg2015.json') as data_2015:
        db2015 = json.load(data_2015)
        data_2015.close()
        db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                            for tweet in db2015
                            if not check_retweet(tweet['text']) and
                            check_best(tweet['text'])], key=lambda x:x[1])
    with open('dbstore15.data', 'w') as outfile:
        pickle.dump(db_sorted, outfile)

EVENTS_AWARDS = []
DIVIDE_FACTOR = 350  #1000

#### Awards Parsing ####
def check_word(token):
    ## Currently not using this-> massive peformance decrease
    '''Returns false if string contains spelling errors'''
    if token in nltk.corpus.words.words(): return True
    return False

def check_stopword(token):
    if token in nltk.corpus.stopwords.words('english'): return True
    return False


def check_name(token):
    if token in nltk.corpus.names.words(): return True
    return False


def count_tokens(string):
    count = 0
    for char in string:
        if char.isspace(): count+=1
    return count


def get_awards_matches(db, i, num_tweets):
    '''[JSON DB] db, [U_Int] i, [U_Int] num_tweets -> List-of Matches'''
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
            print award[0], string
            if difflib.SequenceMatcher(None, award[0], string).ratio() >= .8:
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
            else:
                match[1] += 1
                return
        matches.append([results_str, 1]) #if no match append
    def trim_award(string):
        # Trim a string before colon
        ret_str = ""
        for n in range(0, len(string)):
            if (not string[n].isalpha() and not string[n].isspace()):   # == ":" or string[n] == "-"
                if (string[n] != ","): #and string[n] != "-"):
                    return ret_str
            ret_str += string[n]
        return ret_str
    event_i = get_event_indicies(get_tpm_arr(db), len(db)/DIVIDE_FACTOR)[i]
    matches = []
    for n in range(0,num_tweets):
        results_str = "Best "
        tweet_i = event_i + n
        tweet = ""
        tweet = db[tweet_i][0]
        find_i = tweet.find("Best")
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
                if (tmp_word == "tv"):
                    results_str += "Television "
                elif (tmp_word == "film" or tmp_word == "movie" or tmp_word == "motion"):
                    results_str += "Motion Picture "
                elif (tmp_word == "picture"): continue
 #               elif (tmp_word == "film" or tmp_word == "movie"):
  #                  results_str += "Motion Picture "
                elif (tmp_word == "in"):
                    results_str = results_str[:-1] + ", "
                elif (tmp_word == "foreign"):
                    results_str += "Foreign Language "
                elif (tmp_word == "language"): continue
                elif (tmp_word.find("min") != -1):
                    results_str += "Mini-Series "
                elif (tmp_word.find("dress") != -1): break
                elif (tmp_word == "comedy" or tmp_word == "musical"):
                    j = len(results_str)-1
                    while j >= 0:
                        if results_str[j-1].isalpha():
                            break
                        j-=1
                    results_str = results_str[:j] + ", Comedy or Musical "
                    break
                elif (tmp_word == "drama"):
                    j = len(results_str)-1
                    while j >= 0:
                        if results_str[j-1].isalpha():
                            break
                        j-=1
                    results_str = results_str[:j] + ", Drama "
                    break
                elif (tmp_word == "a"): continue
                elif (tmp_word == "feature"): continue
                else:
                    results_str += word + " "
       # results_str = check_television(results_str)
        if (results_str != ""):
            results_str = trim_award(results_str)
            find_and_cut_or_add(matches, results_str, find_i)
    return matches

def check_television(string):
    s = nltk.word_tokenize(string)
    istv = False
    for word in s:
        if word.lower() == "television":
            istv = True
    if(istv):
        has_made = False
        for word in s:
            if word.lower() == "made":
                has_made = True
                print s
        if not has_made:
            print s
            return " "
    return string

def most_common_match(db, i, num_tweets):
    ga = get_awards_matches(db,i,num_tweets)
    if ga == []:
        return False
    else:
        return sorted(ga, key=lambda x:x[1], reverse=True)[0] #:2

def remove_similar(vec):
    for awardA, awardB in itertools.combinations(vec, 2):
        if difflib.SequenceMatcher(None, awardA[0], awardB[0]).ratio() >= 0.85:
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
    EVENTS = get_event_indicies(get_tpm_arr(db), len(db)/DIVIDE_FACTOR)
    DIST_ADDR = 0
    for n in range (1, len(EVENTS)):
        DIST_ADDR += EVENTS[n] - EVENTS[n-1]
        
    DISTANCE_BETWEEN_EVENTS = DIST_ADDR/(len(EVENTS)-1)
    NUM_EVENTS = len(EVENTS)
    stripped_vec = []
    for n in range(0,NUM_EVENTS-1):
        most_common = most_common_match(db, n, DISTANCE_BETWEEN_EVENTS)
        if most_common: EVENTS_AWARDS.append(most_common)
    remove_similar2(remove_similar(EVENTS_AWARDS))
    for award in EVENTS_AWARDS:
        c_string = award[0].split()
        c_string[len(c_string)-1]
        if award[1] > 2 and c_string[len(c_string)-1][0].isupper(): #ensure ending on caps
    #        print award
            stripped_vec.append(award[0])
    stripped_vec = format_output(stripped_vec)
   # for award in stripped_vec:
   #     print award
    return stripped_vec

def strip_propers_award(s):
    '''Returns a list proper nouns from a list-of Tokens'''
    proper_nouns = []
    noun_group = ""
    curr_size =0
    for token in s:
        if (token[0].isupper()) or token[0] == '\'' or token[0] == '\"':
            noun_group += token + " "
            curr_size += 1
            if token[len(token) - 1] == '\'' or token[len(token) - 1] == '\"':
                proper_nouns.append(noun_group)
                noun_group = ""
        if(curr_size >=2):
            proper_nouns.append(noun_group)
            noun_group = ""
            curr_size =0
        else:
            if(noun_group == ""): continue
            else:
                proper_nouns.append(noun_group)
                noun_group = ""
    if(noun_group != ""): proper_nouns.append(noun_group)
    return proper_nouns



def rejoin(lst):
    ret_str = ""
    for word in lst:
        ret_str += word + " "
    return ret_str
        
def find_best_dressed(db):
    bigrams_l = []
    def remove_award_name(string):
        ret_str=""
        t_l = [token for token in nltk.word_tokenize(string)]
        for token in t_l:
            if token.find("Red") != -1: continue
            if token.find("See") != -1: continue
            if token.find("Dress") != -1: continue
            if  token.find("Best") != -1: continue
            if token.find("dress") != -1: continue
            if  token.find("best") != -1: continue
            if token.find("worst") != -1: return ""
            if  token.find("Worst") != -1: return ""
            if token.find("Golden") != -1: continue
            if  token.find("Globes") != -1: continue
            if check_stopword(token): continue
            if check_name(token): 
                ret_str += token + " "
        return ret_str
    for tweet in db:
        tweet_text = tweet[0]
        dress_loc = tweet_text.lower().find("dress")
        if dress_loc != -1:
            stripped = strip_propers_award(nltk.word_tokenize(remove_award_name(tweet_text)))
            for gram in nltk.bigrams(stripped):
                bigrams_l.append(gram)
    most_freq  = nltk.FreqDist(bigrams_l).most_common(1)
    ret_str = ""
    for token in most_freq[0][0]:
        ret_str += token
    return ret_str


def find_best_joke(db):
    bigrams_l = []
    def remove_award_name(string):
        ret_str=""
        t_l = [token for token in nltk.word_tokenize(string)]
        for token in t_l:
            if token.find("Red") != -1: continue
            if token.find("See") != -1: continue
            if token.find("Dress") != -1: continue
            if  token.find("Best") != -1: continue
            if token.find("dress") != -1: continue
            if  token.find("best") != -1: continue
            if token.find("worst") != -1: return ""
            if  token.find("Worst") != -1: return ""
            if token.find("Golden") != -1: continue
            if  token.find("Globes") != -1: continue
            if check_stopword(token): continue
            if check_name(token): 
                ret_str += token + " "
        return ret_str
    for tweet in db:
        tweet_text = tweet[0]
        dress_loc = tweet_text.lower().find("joke")
        if dress_loc != -1:
            stripped = strip_propers_award(nltk.word_tokenize(remove_award_name(tweet_text)))
            for gram in nltk.bigrams(stripped):
                bigrams_l.append(gram)
    most_freq  = nltk.FreqDist(bigrams_l).most_common(1)
    ret_str = ""
    for token in most_freq[0][0]:
        ret_str += token
    return ret_str


def find_best_act(db):
    bigrams_l = []
    def remove_award_name(string):
        ret_str=""
        t_l = [token for token in nltk.word_tokenize(string)]
        for token in t_l:
            if token.find("Red") != -1: continue
            if token.find("See") != -1: continue
            if token.find("Dress") != -1: continue
            if  token.find("Best") != -1: continue
            if token.find("dress") != -1: continue
            if  token.find("best") != -1: continue
            if token.find("worst") != -1: return ""
            if  token.find("Worst") != -1: return ""
            if token.find("Golden") != -1: continue
            if  token.find("Globes") != -1: continue
            if check_stopword(token): continue
            if check_name(token): 
                ret_str += token + " "
        return ret_str
    for tweet in db:
        tweet_text = tweet[0]
        dress_loc = tweet_text.lower().find("joke")
        if dress_loc != -1:
            stripped = strip_propers_award(nltk.word_tokenize(remove_award_name(tweet_text)))
            for gram in nltk.bigrams(stripped):
                bigrams_l.append(gram)
    most_freq  = nltk.FreqDist(bigrams_l).most_common(1)
    ret_str = ""
    for token in most_freq[0][0]:
        ret_str += token
    return ret_str