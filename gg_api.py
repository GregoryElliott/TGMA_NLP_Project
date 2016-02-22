import json
import time
import nltk
#from nltk.book import FreqDist
from collections import Counter
from nltk import FreqDist
from nltk.corpus import names
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import trigrams
from nltk.tokenize import *
import re
import string
import pickle
import os.path
from awards_parse import *

IGNORE_WORDS = ['best', 'look', 'television', 'tv', 'movie', 'musical', 'globes', 'congrats', 'congratulations', 'globe', 'i\'m', 'motion', 'picture', 'actor', 'actress', 'drama', 'comedy', 'rt', 'demille', 'award']
    
OFFICIAL_AWARDS = [
    'cecil b. demille award',
    'best motion picture - drama',
    'best performance by an actress in a motion picture - drama',
    'best performance by an actor in a motion picture - drama',
    'best motion picture - comedy or musical',
    'best performance by an actress in a motion picture - comedy or musical',
    'best performance by an actor in a motion picture - comedy or musical',
    'best animated feature film', 'best foreign language film',
    'best performance by an actress in a supporting role in a motion picture',
    'best performance by an actor in a supporting role in a motion picture',
    'best director - motion picture', 'best screenplay - motion picture',
    'best original score - motion picture', 'best original song - motion picture',
    'best television series - drama',
    'best performance by an actress in a television series - drama',
    'best performance by an actor in a television series - drama',
    'best television series - comedy or musical',
    'best performance by an actress in a television series - comedy or musical',
    'best performance by an actor in a television series - comedy or musical',
    'best mini-series or motion picture made for television',
    'best performance by an actress in a mini-series or motion picture made for television',
    'best performance by an actor in a mini-series or motion picture made for television',
    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

REGEX_AWARDS = {
'cecil b. demille award': re.compile(r'((cecil)|(cecil demille)|(cecil b. demille)|(b. demille)|(demille))( award)?', re.IGNORECASE),
'best motion picture - drama': re.compile(r'(golden globe for )?best motion picture(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best motion picture - comedy or musical': re.compile(r'(golden globe for )?best motion picture(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
'best performance by an actress in a motion picture - drama': re.compile(r'best( performance by an)? actress(( in a)|( -))?( motion picture)?(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best performance by an actor in a motion picture - drama': re.compile(r'best( performance by an)? actor(( in a)|( -))?( motion picture)?(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best performance by an actress in a motion picture - comedy or musical': re.compile(r'best( performance by an)? actress(( in a)|( -))?( motion picture)?(,)?(:)?( )?(-)? (musical or )?comedy', re.IGNORECASE),
'best performance by an actor in a motion picture - comedy or musical': re.compile(r'best( performance by an)? actor(( in a)|( -))?( motion picture)?(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
'best performance by an actress in a supporting role in a motion picture': re.compile(r'best( supporting)?( performance by an)? actress( in a)?( supporting)?( role)?( in a)?(,)?(:)?( )?(-)?( motion picture)?', re.IGNORECASE),
'best performance by an actor in a supporting role in a motion picture': re.compile(r'best( supporting)?( performance by an)? actor( in a)?( supporting)?( role)?( in a)?(,)?(:)?( )?(-)?( motion picture)?', re.IGNORECASE),
'best director - motion picture': re.compile(r'best director(,)?(:)?( )?(-)?( motion)?( picture)?', re.IGNORECASE),
'best screenplay - motion picture': re.compile(r'best screenplay(,)?(:)?( )?(-)?( motion)?( picture)?', re.IGNORECASE),
'best animated feature film': re.compile(r'best animated( feature)?( film)?', re.IGNORECASE),
'best foreign language film': re.compile(r'best ((foreign)|(foreign film)|(foreign language)|(foreign language film))', re.IGNORECASE),
'best original score - motion picture': re.compile(r'(golden globe for )?best (original )?score', re.IGNORECASE),
'best original song - motion picture': re.compile(r'(golden globe for )?best (original )?song', re.IGNORECASE),
'best television series - drama': re.compile(r'best ((television)|(TV))( series)?(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best television series - comedy or musical': re.compile(r'best ((television)|(TV))( series)?(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
'best mini-series or motion picture made for television': re.compile(r'best ((((TV)|(television)) ((mini-series)|(miniseries)|(miniseries or motion picture)|(mini-series or motion picture)|(motion picture)))|(((mini-series)|(miniseries)|(miniseries or motion picture)|(mini-series or motion picture)|(motion picture))( made for)? ((television)|(TV))))', re.IGNORECASE),
'best performance by an actress in a mini-series or motion picture made for television': re.compile(r'best( performance)?( by an)? actress( in)?( a)?(,)? ((mini-series)|(miniseries)|(miniseries or motion picture)|(mini-series or motion picture)|(motion picture))( made for)?((/)|( ))?(or )?((television)|(TV))', re.IGNORECASE),
'best performance by an actor in a mini-series or motion picture made for television': re.compile(r'Best( performance)?( by an)? actor( in)?( a)? ((mini-series)|(miniseries)|(miniseries or motion picture)|(mini-series or motion picture)|(motion picture))( made for)?((/)|( ))?( or)?((television)|(TV))', re.IGNORECASE),
'best performance by an actress in a television series - drama': re.compile(r'best( performance)?( by an)? actress( in a)? ((television)|(TV))( series)?(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best performance by an actor in a television series - drama': re.compile(r'best( performance)?( by an)? actor( in a)? ((television)|(TV))( series)?(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best performance by an actress in a television series - comedy or musical': re.compile(r'best( performance)?( by an)? actress( in a)?(,| )?((television)|(TV))( series)?(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
'best performance by an actor in a television series - comedy or musical': re.compile(r'best( performance)?( by an)? actor( in a)?(,| )?((television)|(TV))( series)?(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': re.compile(r'best( supporting)?( performance by an)? actress( in a)?( supporting)?( role)?( in a)?(,)?(:)?( )?(-)?( motion picture)?( series)?( mini-series)?( for)?((television)|(TV))', re.IGNORECASE),
'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': re.compile(r'best( supporting)?( performance by an)? actor( in a)?( supporting)?( role)?( in a)?(,)?(:)?( )?(-)?( motion picture)?( series)?( mini-series)?( for)?((television)|(TV))', re.IGNORECASE)}

#### ---------------------- Internal Functions ------------------------- ####

with open('gg2013.json') as data_2013:
    db2013 = json.load(data_2013)

TPM_THRESHOLD = 500

def get_time(db, i):
    '''Returns a list of [Hour, Minutes] for a tweet at index i in db'''
    def get_hour_minutes(time):
        return [time[3], time[4]]
    return get_hour_minutes(time.gmtime(int(db[i]["timestamp_ms"])/1000))


def get_tpm_arr(db):
    '''Returns a TPM (Tweet-per-minute) array for the given db'''
    dim = db[len(db)-1][1]
    freq_table = [[[0,0] for i in range(60)] for j in range(dim[0]+1)]
    ittr = 0
    for n in db:
        curr_time = n[1]
        # Either create a new entry or increment old one
        if (freq_table[curr_time[0]][curr_time[1]] == [0,0]):
            freq_table[curr_time[0]][curr_time[1]] = [1, ittr]
        else:
            freq_table[curr_time[0]][curr_time[1]][0] += 1
            ittr+=1
    return freq_table


def get_event_indicies(tpm_arr):
    '''Returns the indicies of events that meet the TPM_THRESHOLD'''
    lst = []
    for r in tpm_arr:
        for n in r:
            if n[0] >= TPM_THRESHOLD:
                lst.append(n[1])
    return lst


def normalize_str(s):
    '''Returns a normalized string with the first letter lowercase'''
    ns = ""
    ns += s[0]
    for i in range(1, len(s)):
        ns += s[i]

    return ns


def strip_propers(s):
    '''Returns a list proper nouns from a list-of Tokens'''
    proper_nouns = []
    noun_group = ""
    quotes = False
    for token in s:
        if token in IGNORE_WORDS:
            if(noun_group == ""): continue
            else:
                proper_nouns.append(noun_group.replace('\'','\"'))
                noun_group = ""
        if (token[0].isupper()) or token[0] == '\'' or token[0] == '\"' or quotes or token[0].strip(' ').isdigit():
            noun_group += token + " "
            if '\'s' in noun_group:
                noun_group = noun_group.replace('\'s','')
            if token[0] == '\'' or token[0] == '\"':
                quotes = True
                if noun_group == "":
                    noun_group = token + " "
                else:
                    proper_nouns.append(noun_group.replace('\'','\"'))
                    noun_group = token + " "
            if token[len(token) - 1] == '\'' or token[len(token) - 1] == '\"':
                proper_nouns.append(noun_group)
                noun_group = ""
                quotes = False
            if token[0].isdigit():
                proper_nouns.append(noun_group.replace('\'','\"'))
                noun_group = ""
            if noun_group.count(".") == 1:
                noun_group = noun_group.replace(".", "")
            for punct in [',',':','!',';','/']:      
                if punct in noun_group:
                    noun_group = noun_group.replace(punct, "")
                    proper_nouns.append(noun_group.replace('\'','\"'))
                    noun_group = ""
        else:
            if(noun_group == ""): continue
            else:
                proper_nouns.append(noun_group.replace('\'','\"'))
                noun_group = ""
    if(noun_group != ""): proper_nouns.append(noun_group)
    return proper_nouns

def strip_proper_pairs(s):
    '''Returns a list proper nouns from a list-of Tokens'''
    proper_nouns = []
    noun_group = ""
    for token in s:
        if token in IGNORE_WORDS:
            if(noun_group == ""): continue
            else:
                proper_nouns.append(noun_group.replace('\'','\"'))
                noun_group = ""
        if (token[0].isupper()) or token == 'and':
            noun_group += token + " "            
        else:
            if(noun_group == ""): continue
            for punct in [',','.',':','!',';','/']:      
                if punct in noun_group:
                    noun_group = noun_group.replace(punct, "")                    
            proper_nouns.append(noun_group.replace('\'','\"'))
            noun_group = ""
    if(noun_group != ""): proper_nouns.append(noun_group)
    return proper_nouns


def get_variations(s):
    base = s.split()
    variations = []
    for n in base:
        if n in names.words():
            variations.append(n)
        if s in names.words():
            variations.append(s)
    return variations

def get_pn_vec_from_range(db):
    events = []
    matches = -1
    nominees = {}
    winners = {}
    for event_index in get_event_indicies(get_tpm_arr((db))):   
        pn_count_vec = []
        bigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in bigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        trigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in trigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        name = bigram + trigram
        pn_count_vec = FreqDist(name)
        events.append(pn_count_vec)

    return events

def get_pn_vec_from_range_for_hosts(db):
    events = []
    matches = -1
    nominees = {}
    winners = {}
    for event_index in get_event_indicies(get_tpm_arr((db))):   
        pn_count_vec = []
        bigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in bigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        trigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in trigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        name = bigram + trigram
        pn_count_vec = FreqDist(name)
        events.append(pn_count_vec)
    return events


### Awards Parsing  
### Depends On: Nothing
########################################################################
#EVENTS = get_event_indicies(get_tpm_arr(db2013))
#NUM_EVENTS = len(EVENTS)

#### Functions for String-Index-Vectors ####
#### Ex: "This is a sentence -> [0, 5, 8, 10, 19]
def get_string_indicies(string):
    '''Returns a String-Index-Vector for a given string'''
    indicies_vec = [0]                  # init with str start
    for n in range(0,len(string)):
        if (string[n] == " "):
            indicies_vec.append(n+1)
    indicies_vec.append(len(string)+1)  # pushback ending pos
    return indicies_vec


def get_len(indicies_vec):
    '''Returns the number of words given a String-Index-Vector'''
    return len(indicies_vec) - 1


def get_word(i, indicies_vec, string):
    '''Returns the word at index i given a String-Index-Vector and a string'''
    return string[indicies_vec[i]:(indicies_vec[i+1]-1)]


def find_ind(i, indicies_vec):
    for n in range(0,len(indicies_vec)):
        if (indicies_vec[n] == i): return n
    return -1

        
#### Awards Parsing ####
def get_awards_matches(db, i, num_tweets):
    '''[JSON DB] db, [U_Int] i, [U_Int] num_tweets -> List-of Matches'''
    MIN_MATCH_THRESHOLD = 30
    WORD_GRAB_COUNT = 10
    def find_and_cut_or_add(matches_vec, string, start_i):
        for match in matches_vec:
            ind = 0
            for n in range(0, len(string)):
                ind +=1
                if (n >= (len(match[0])-1)): break
                if (string[n] != match[0][n]): break
            if (ind < MIN_MATCH_THRESHOLD): continue #Skip if not really a match
            else:
                match[0] = match[0][:ind]
                match[1] += 1
                return
        matches.append([results_str, 1]) #if no match append
    event_i = get_event_indicies(get_tpm_arr((db)))[i]
    matches = []
    for n in range(0,num_tweets):
        results_str = "Best "
        tweet_i = event_i + n
        tweet = ""
        tweet = db[tweet_i]['text']
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
                results_str += word + " "
        if (results_str != ""):
            find_and_cut_or_add(matches, results_str, find_i)
    return matches

def most_common_match(db, i, num_tweets):
    return sorted(get_awards_matches(db,i,num_tweets), key=lambda x:x[1], reverse=True)[1]



#### ---------------------- API Accesing Functions ------------------------- ####


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    file_name = 'gg%s.json' % year
    with open(file_name, 'r') as data:
        db = json.load(data)
    hosts = []
    pairs = []
    for f in db:
        e = f['text']
        if 'and' in e.lower():
            for proper in strip_proper_pairs(normalize_str(e).split()):
                pair = proper.split('and')
                if len(pair) == 2:
                    if pair[0] != ' ' and pair[1] != ' ':
                        pairs.append((pair[0].lower().replace('\'','\"').strip(' '), pair[1].lower().replace('\'','\"').strip(' ')))
    pairs_freq = FreqDist(pairs)
    if len(pairs_freq.most_common(10)[0][0][0].split(' ')) < 2:
        hosts.append(pairs_freq.most_common(10)[1][0][0])
        hosts.append(pairs_freq.most_common(10)[1][0][1])
    else:
        hosts.append(pairs_freq.most_common(10)[0][0][0])
        hosts.append(pairs_freq.most_common(10)[0][0][1])
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    year = year[2:4]    
    file_name = 'dbstore%s.data' % year
    with open(file_name) as infile:
        db = pickle.load(infile)

    ret_l = p_most_common(db)
    return ret_l

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    yr = year[2:4]
    file_name = 'nrt_dbstore%s.data' % yr
    with open(file_name) as infile:
        db = pickle.load(infile)
        
    lower_names = []
    for n in names.words():
        lower_names.append(n.lower())
    nominees = {}
    presenters = get_presenters(year)
    for award in REGEX_AWARDS:
        nominees[award] = []
    winn = get_winner(year)
    hosts = get_hosts(year)
    for event_index in get_event_indicies(get_tpm_arr((db))):
        award = None
        propers = []
        awards = []
        for n in range(500):
            e = db[event_index + n][0]
            if 'RT' in e:
                continue
            for a in REGEX_AWARDS:
                if re.search(REGEX_AWARDS[a], e.lower()): 
                    awards.append(a)
            for a in winn:                    
                if winn[a] in e.lower(): 
                    awards.append(a)
            for proper in strip_propers(normalize_str(e).split()):
                propers.append(proper)

        if len(awards) == 0:
            continue
        awards_freq = FreqDist(awards)
        award = awards_freq.most_common(1)[0][0]
        freq = FreqDist(propers)    
        count = 0
        done = False

        for g in freq.most_common(200):
            g = (g[0].strip(' '), g[1])
            stop = False
            if 'the' == g[0].lower():
                continue
            if g[0] == '':
                continue
            if 'film' in award:                 
                if len(g[0].split(' ')) < 2:
                    if g[0].count('\'') != 2 and g[0].count('\"') != 2:
                        continue
            if 'actor' in award or 'actress' in award or 'director' in award: 
                if len(g[0].split(' ')) < 2:
                    continue
                if g[0].lower().split(' ')[0] not in lower_names and g[0].lower().split(' ')[1] not in lower_names:
                    continue
            if g[0] == 'I':
                continue
            for host in hosts:
                if g[0].lower() in host or host in g[0].lower():
                    stop = True
                    break
            for w in winn:
                if g[0].lower() in winn[w] or winn[w] in g[0].lower():
                    stop = True
                    break
            for p in presenters:
                for pres in presenters[p]:
                    if g[0].lower() in pres or pres in g[0].lower():
                        stop = True
                        break
            for ignore in IGNORE_WORDS:
                if ignore in g[0].lower():                      
                    stop = True
                    break
            for nom in nominees[award]:
                if nom.lower() in g[0].lower() or g[0].lower() in nom.lower():
                    stop = True
                    break
            if 'the' == g[0].lower():
                continue
            if 'i ' in g[0].lower():
                continue
            if stop: 
                continue
            if len(nominees[award]) >= 4:
                done = True
                break
            if 'best' in g[0].lower() or 'award' in g[0].lower():
                continue
            nominees[award].append((g[0].lower().strip("\"")))
            break
        
    return nominees

def get_winner(year):
    lower_names = []
    for n in names.words():
        lower_names.append(n.lower())
    lower_names.append('simmons')
    file_name = 'gg%s.json' % year
    with open(file_name, 'r') as data:
        db = json.load(data)
    awards = OFFICIAL_AWARDS
    winners = {}
    winners_list = {}
    winners_freq = {}
    hosts = get_hosts(year)
    reg = REGEX_AWARDS
    propers = []

    for award in awards:
        winners_list[award] = []
    for award in reg: 
        award_str = []        
        for f in db:
            e = f['text']
            if 'RT' in e:
                continue            
            if 'supporting' not in award:
                if 'supporting' in e.lower():
                    continue
            if 'supporting' in award:
                if 'supporting' not in e.lower():
                    continue    
            if 'supporting role in a motion picture' in award:
                if 'miniseries' in e.lower() or 'mini-series' in e.lower():
                    continue                
            if re.search(reg[award],e.lower()): 
                for proper in strip_propers(normalize_str(e).split()):    
                    if 'song' in award:
                        regexpr1 = 'film %s' % proper
                        regexpr2 = 'film \'%s' % proper
                        regexpr3 = 'film \"%s' % proper 
                        regexpr4 = 'movie %s' % proper
                        regexpr5 = 'movie \'%s' % proper
                        regexpr6 = 'movie \"%s' % proper 
                        regexpr7 = 'from %s' % proper
                        regexpr8 = 'from \'%s' % proper
                        regexpr9 = 'from \"%s' % proper 
                        if regexpr1.lower() in e.lower() or regexpr2.lower() in e.lower() or regexpr3.lower() in e.lower() or regexpr4.lower() in e.lower() or regexpr5.lower() in e.lower() or regexpr6.lower() in e.lower() or regexpr7.lower() in e.lower() or regexpr8.lower() in e.lower() or regexpr9.lower() in e.lower():
                            winners_list[award].append(proper.lower().replace('\'','\"').strip(' '))
                    else:
                        winners_list[award].append(proper.lower().replace('\'','\"').strip(' '))
                continue

    test_winners_list = {}
    for a in winners_list:
        freq = FreqDist(winners_list[a])
        winners_freq[a] = freq
        test_winners_list[a] = []
    
    for h in winners_freq:
        done = False
        for win in winners_freq[h].most_common(25):                        
            stop = False
            if 'the' == win[0].lower():
                continue
            if win[0] == '':
                continue
            for a in h.split(' '):                       
                if 'film' in h:                 
                    if len(win[0].split(' ')) < 2:
                        if win[0].count('\'') != 2 and win[0].count('\"') != 2:
                            for cur_win in winners_freq[h].most_common(25):
                                if win[0] in cur_win[0] and len(cur_win[0].split(' ')) > 2:
                                    if cur_win[0][0] == '\'' or cur_win[0][0] == '\"':
                                        if cur_win[0][len(cur_win[0])-1] == '\'' or cur_win[0][len(cur_win[0])-1] == '\"':
                                            win = cur_win                                   
                                            break     
                if 'actor' in h or 'actress' in h or 'director' in h:                    
                    replace = False
                    if len(win[0].split(' ')) < 2:
                        for cur_win in winners_freq[h].most_common(25):
                            if cur_win[0] == '':
                                continue
                            if win[0] in cur_win[0] and len(cur_win[0].split(' ')) == 2:
                                win = cur_win
                                replace = True
                                break
                        if not replace:
                            break
                    if not replace:
                        if win[0].split(' ')[0] not in lower_names and win[0].split(' ')[1] not in lower_names:
                            break
                if a.lower() in win[0].lower():
                    break
                for ignore in IGNORE_WORDS:
                    if ignore in win[0].lower():                      
                        stop = True
                        break
                for host in hosts:
                    if host.lower() in win[0]:
                        stop = True
                        break
                if 'song' in h or 'screenplay' in h or 'score' in h:
                    if win[0].count('\'') != 2 and win[0].count('\"') != 2:
                        break                            
                if stop:
                    break   
                if not done:
                    winners[h] = (win[0].strip("\"")) 
                test_winners_list[h].append(win)
                done = True
                break
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    lower_names = []
    for n in names.words():
        lower_names.append(n.lower())
    file_name = 'gg%s.json' % year
    with open(file_name, 'r') as data:
        db = json.load(data)
    presenters = []
    awards = OFFICIAL_AWARDS
    presenters = {}
    winners_list = {}
    winners_freq = {}
    hosts = get_hosts(year)
    reg = REGEX_AWARDS
    propers = []
    winn = get_winner(year)

    for award in awards:
        winners_list[award] = []
    for award in reg: 
        award_str = []
        for f in db:
            e = f['text']
            if 'RT' in e:
                continue
            if 'supporting' not in award:
                if 'supporting' in e.lower():
                    continue
            if 'supporting' in award:
                if 'supporting' not in e.lower():
                    continue
            if re.search(r'\spresent(s)?(er)?', e.lower()):                   
                if re.search(reg[award],e.lower()): 
                    for proper in strip_propers(normalize_str(e).split()):
                        winners_list[award].append(proper.lower().replace('\'','\"').strip(' '))
                    continue
        test_winners_list = {}
    count = 0
    for f in db:
        e = f['text']
        if re.search(r'\s(a)?present(s)?(er)?', e.lower()):
            for win in winn:
                if winn[win] in e.lower():
                    for proper in strip_propers(normalize_str(e).split()):
                        if winn[win] not in proper:
                            winners_list[win].append(proper.lower().replace('\'','\"').strip(' '))
    pairs = []
    for f in db:
        e = f['text']
        if 'and' in e.lower():
            for proper in strip_proper_pairs(normalize_str(e).split()):
                pair = proper.split('and')
                if len(pair) == 2 and len(pair[0].split(' ')) == 2 and len(pair[1].split(' ')) == 2:
                    if pair[0] not in hosts and pair[1] not in hosts and pair[0] != ' ' and pair[1] != ' ':
                        pairs.append((pair[0].lower().replace('\'','\"').strip(' '), pair[1].lower().replace('\'','\"').strip(' ')))
    pairs_freq = FreqDist(pairs)
    for a in winners_list:
        freq = FreqDist(winners_list[a])
        winners_freq[a] = freq
        presenters[a] = [] 
        test_winners_list[a] = []
    
    for h in winners_freq:
        count = 0
        done = False
        for win in winners_freq[h].most_common(25):            
            stop = False
            if 'the' == win[0].lower():
                continue
            if winn[h].lower() in win[0].lower():
                stop = True
                continue
            for pair in pairs_freq.most_common(50):
                if win[0].lower() in pair:
                    done = True
                    presenters[h].append(pair[0])
                    presenters[h].append([pair[1]])
            if '...' in win[0]:
                continue
            if 'presents' in win[0].lower():
                win = ((win[0].lower().split("presents"))[0], win[1])
            if 'presented by' in win[0].lower():
                win = ((win[0].lower().split("presented by"))[1], win[1])
            if 'present' in win[0].lower():
                win = ((win[0].lower().split("present"))[0], win[1])
            if any(char.isdigit() for char in win[0]):
                continue
            for a in h.split(' '):           
                if a.lower() in win[0].lower():
                    break
                for ignore in IGNORE_WORDS:
                    if ignore in win[0].lower():
                        stop = True
                        break
                for host in hosts:
                    if host in win[0]:
                        stop = True
                        break
                if len(win[0].split(' ')) != 2:
                    break
                if win[0].split(' ')[0] not in lower_names and win[0].split(' ')[1] not in lower_names:
                    break
                if stop:
                    break   
                if not done:
                    presenters[h].append(win[0])
                test_winners_list[h].append(win)
                count = count + 1
                if count >= 2:
                    done = True
                break

    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    
    print "Beginning ceremony processing"

    # Sort and dump python list objects as text files
    if not os.path.exists('dbstore13.data') or not os.path.exists('dbstore15.data'):
        print "Creating dbstore13.data"
        with open('gg2013.json') as data_2013:
            db2013 = json.load(data_2013)
            data_2013.close()
            db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                                for tweet in db2013
                                if not check_retweet(tweet['text']) and
                                check_best(tweet['text'])], key=lambda x:x[1])
        with open('dbstore13.data', 'w') as outfile:
            pickle.dump(db_sorted, outfile)
        print "Creating dbstore15.data"
        with open('gg2015.json') as data_2015:
            db2015 = json.load(data_2015)
            data_2015.close()
            db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                                for tweet in db2015
                                if not check_retweet(tweet['text']) and
                                check_best(tweet['text'])], key=lambda x:x[1])
        with open('dbstore15.data', 'w') as outfile:
            pickle.dump(db_sorted, outfile)
    if not os.path.exists('nrt_dbstore13.data') or not os.path.exists('nrt_dbstore15.data'):
        print "Creating nrt_dbstore13.data"
        with open('gg2013.json') as data_2013:
            db2013 = json.load(data_2013)
            data_2013.close()
            db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                                for tweet in db2013
                                if not check_retweet(tweet['text'])], key=lambda x:x[1])
        with open('nrt_dbstore13.data', 'w') as outfile:
            pickle.dump(db_sorted, outfile)
        print "Creating nrt_dbstore15.data"
        with open('gg2015.json') as data_2015:
            db2015 = json.load(data_2015)
            data_2015.close()
            db_sorted = sorted([[tweet['text'],cnv_time(int(tweet['timestamp_ms']))]
                                for tweet in db2015
                                if not check_retweet(tweet['text'])], key=lambda x:x[1])
        with open('nrt_dbstore15.data', 'w') as outfile:
            pickle.dump(db_sorted, outfile)
    print "Pre-ceremony processing complete."
    return

def get_best_dressed(year):
    year = year[2:4]    
    file_name = 'dbstore%s.data' % year
    with open(file_name) as infile:
        db = pickle.load(infile)
    ret_l = find_best_dressed(db)
    return ret_l

def get_best_joke(year):
    year = year[2:4]    
    file_name = 'dbstore%s.data' % year
    with open(file_name) as infile:
        db = pickle.load(infile)
    ret_l = find_best_joke(db)
    return ret_l

def start_interface():
    def pr_help():
        print "List of commands:"
        print "hosts [year] \t Displays the hosts for a given year"
        print "awards [year] \t Displays the awards for a given year"
        print "nominees [year] \t Displays the nominees for a given year"
        print "winners [year] \t Displays the winners for a given year"
        print "presenters [year] \t Displays the presenters for a given year"
        print "bestdress [year] \t Displays best dressed individual for a given year"
        print "bestjoke [year] \t Displays who gave the best joke for a given year"
        print "help \t Display all available of commands"
        print "exit \t Quits the program"
    def check_year(s):
        if s == "2013" or s == "2015":
            return True
        print "Please enter a valid year"
        return False
    print "Performing database initialization"
    pre_ceremony()
    print "Welcome to GG Awards Parser v2.0!"
    print "=========================================="
    print "Enter help for a list of commonly-used commands"
    print "Special features include: Best Dressed and Best Joke"
    print "Databases available: 2013, 2015"
    print "========================================="
    while True:
        s_input = raw_input()
        tokens = s_input.split()
        if len(tokens) > 2:
            print "Unknown command. Type help for commands list or exit to quit"
        elif len(tokens) < 2:
            if tokens[0] == "help":
                pr_help()
            elif tokens[0] == "exit":
                return
            else:
                print "Unknown command. Type help for commands list or exit to quit"
        else:
            if tokens[0] == "hosts":
                if check_year(tokens[1]):
                    print "Fetching hosts..."
                    hosts = get_hosts(tokens[1])
                    for host in hosts:
                        print host
            elif tokens[0] == "nominees":
                if check_year(tokens[1]):
                    print "Fetching nominees..."
                    nominees = get_nominees(tokens[1])
                    for nominee in nominees:
                        print ""
                        print nominee, ":"
                        for n in nominees[nominee]:
                            print n
            elif tokens[0] == "awards":
                if check_year(tokens[1]):
                    print "Fetching awards..."
                    awards = get_awards(tokens[1])
                    for award in awards:
                        print award
            elif tokens[0] == "winners":
                if check_year(tokens[1]):
                    print "Fetching winners..."
                    winners = get_winner(tokens[1])
                    for winner in winners:
                        print winner, ": \t", winners[winner]
            elif tokens[0] == "presenters":
                if check_year(tokens[1]):
                    print "Fetching presenters..."
                    presenters = get_presenters(tokens[1])
                    for p in presenters:
                        print ""
                        print p, ":"
                        for n in presenters[p]:
                            print n
            elif tokens[0] == "bestdress":
                if check_year(tokens[1]):
                    print "Fetching best dressed..."
                    print get_best_dressed(tokens[1])
            elif tokens[0] == "bestjoke":
                if check_year(tokens[1]):
                    print "Fetching best joke..."
                    print get_best_joke(tokens[1])
            else:
                print "Unknown command. Type help for commands list or exit to quit"

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    pre_ceremony()
    start_interface()

    return

if __name__ == '__main__':
    main()