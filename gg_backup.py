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
'best performance by an actress in a motion picture - comedy or musical': re.compile(r'best( performance by an)? actress(( in a)|( -))?( motion picture)?(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
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
'best performance by an actress in a mini-series or motion picture made for television': re.compile(r'best( performance)?( by an)? actress( in)?( a)? ((mini-series)|(miniseries)|(miniseries or motion picture)|(mini-series or motion picture)|(motion picture))( made for)?((/)|( ))?(or )?((television)|(TV))', re.IGNORECASE),
'best performance by an actor in a mini-series or motion picture made for television': re.compile(r'Best( performance)?( by an)? actor( in)?( a)? ((mini-series)|(miniseries)|(miniseries or motion picture)|(mini-series or motion picture)|(motion picture))( made for)?((/)|( ))?( or)?((television)|(TV))', re.IGNORECASE),
'best performance by an actress in a television series - drama': re.compile(r'best( performance)?( by an)? actress( in a)? ((television)|(TV))( series)?(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best performance by an actor in a television series - drama': re.compile(r'best( performance)?( by an)? actor( in a)? ((television)|(TV))( series)?(,)?(:)?( )?(-)? drama', re.IGNORECASE),
'best performance by an actress in a television series - comedy or musical': re.compile(r'best( performance)?( by an)? actress( in a)? ((television)|(TV))( series)?(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
'best performance by an actor in a television series - comedy or musical': re.compile(r'best( performance)?( by an)? actor( in a)? ((television)|(TV))( series)?(,)?(:)?( )?(-)? comedy', re.IGNORECASE),
'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': re.compile(r'best( supporting)?( performance by an)? actress( in a)?( supporting)?( role)?( in a)?(,)?(:)?( )?(-)?( motion picture)?( series)?( mini-series)?( for)?((television)|(TV))', re.IGNORECASE),
'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': re.compile(r'best( supporting)?( performance by an)? actor( in a)?( supporting)?( role)?( in a)?(,)?(:)?( )?(-)?( motion picture)?( series)?( mini-series)?( for)?((television)|(TV))', re.IGNORECASE)}

#### ---------------------- Internal Functions ------------------------- ####

with open('gg2013.json') as data_2013:
    db2013 = json.load(data_2013)

TPM_THRESHOLD = 1400

def get_time(db, i):
    '''Returns a list of [Hour, Minutes] for a tweet at index i in db'''
    def get_hour_minutes(time):
        return [time[3], time[4]]
    return get_hour_minutes(time.gmtime(db[i]["timestamp_ms"]/1000))


def get_tpm_arr(db):
    '''Returns a TPM (Tweet-per-minute) array for the given db'''
    dim = get_time(db, len(db)-1)
    freq_table = [[[0,0] for i in range(60)] for j in range(dim[0]+1)]
    ittr = 0
    for n in db:
        curr_time = get_time(db, ittr)
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
            for punct in [',','.',':','!',';','/']:      
                if punct in noun_group:
                    noun_group = noun_group.replace(punct, "")
                    proper_nouns.append(noun_group.replace('\'','\"'))
                    noun_group = ""
            #if '-' in noun_group:
                #noun_group = noun_group.replace('-', ' ')
        else:
            if(noun_group == ""): continue
            else:
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
    #pn_count_vec = [["none", 0]]
    events = []
    #event_index = get_event_indicies(get_tpm_arr((db)))[1]
    matches = -1
    #for event_index in get_event_indicies(get_tpm_arr((db))):
        #for n in range(0,100):
            #tweet_index = event_index + n
            #for proper in strip_propers(normalize_str(db[tweet_index]['text']).split()):
                #for variation in get_variations(proper):
                    #for i in range(0, len(pn_count_vec)):
                        #if pn_count_vec[i][0].find(variation) != -1:
                            #matches = i
                            #break
                #if (matches == -1):
                    #pn_count_vec.append([proper,0])
                #else:
                    #pn_count_vec[matches][1] += 1
                    #matches = -1
            #print strip_propers(normalize_str(db[tweet_index]['text']).split())
    #j = 0
    nominees = {}
    winners = {}
    for event_index in get_event_indicies(get_tpm_arr((db))):
        #if j > 6:
            #break
        pn_count_vec = []
        #content = [proper for n in range(0,1000) for proper in strip_propers(normalize_str(db[event_index + n]['text']).split()) if proper[0].strip().lower() not in stopwords.words()]
        #content = [proper for n in range(0,1000) for proper in strip_propers(normalize_str(db[event_index + n]['text']).split())]
        #content = [b for n in range(0,1000) for b in db[event_index + n]['text'].split()]
        bigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in bigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        trigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in trigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        #bigram = bigrams(word_tokenize(content))
        name = bigram + trigram
        pn_count_vec = FreqDist(name)
        #pn_temp = FreqDist(name)

            #for variation in get_variations(item[0]):
                #if variation in pn_count_vec:
                    #pn_count_vec[item[0]] = pn_count_vec[item[0]] + pn_count_vec[variation]
        events.append(pn_count_vec)
        #j = j + 1

    return events

def get_pn_vec_from_range_for_hosts(db):
    #pn_count_vec = [["none", 0]]
    events = []
    #event_index = get_event_indicies(get_tpm_arr((db)))[1]
    matches = -1
    #for event_index in get_event_indicies(get_tpm_arr((db))):
        #for n in range(0,100):
            #tweet_index = event_index + n
            #for proper in strip_propers(normalize_str(db[tweet_index]['text']).split()):
                #for variation in get_variations(proper):
                    #for i in range(0, len(pn_count_vec)):
                        #if pn_count_vec[i][0].find(variation) != -1:
                            #matches = i
                            #break
                #if (matches == -1):
                    #pn_count_vec.append([proper,0])
                #else:
                    #pn_count_vec[matches][1] += 1
                    #matches = -1
            #print strip_propers(normalize_str(db[tweet_index]['text']).split())
    #j = 0
    nominees = {}
    winners = {}
    for event_index in get_event_indicies(get_tpm_arr((db))):
        #if j > 6:
            #break
        pn_count_vec = []
        #content = [proper for n in range(0,1000) for proper in strip_propers(normalize_str(db[event_index + n]['text']).split()) if proper[0].strip().lower() not in stopwords.words()]
        #content = [proper for n in range(0,1000) for proper in strip_propers(normalize_str(db[event_index + n]['text']).split())]
        #content = [b for n in range(0,1000) for b in db[event_index + n]['text'].split()]
        bigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in bigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        trigram = [w for n in range(500) for s in sent_tokenize(db[event_index + n]['text']) for w in trigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
        #bigram = bigrams(word_tokenize(content))
        name = bigram + trigram
        pn_count_vec = FreqDist(name)
        #pn_temp = FreqDist(name)

            #for variation in get_variations(item[0]):
                #if variation in pn_count_vec:
                    #pn_count_vec[item[0]] = pn_count_vec[item[0]] + pn_count_vec[variation]
        events.append(pn_count_vec)
        #j = j + 1

    return events


### Awards Parsing  
### Depends On: Nothing
########################################################################
EVENTS = get_event_indicies(get_tpm_arr(db2013))
NUM_EVENTS = len(EVENTS)

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

def p_most_common():
    for n in range(0,NUM_EVENTS-1):
        print most_common_match(db2013, n, 1000)



#### ---------------------- API Accesing Functions ------------------------- ####


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    file_name = 'gg%s.json' % year
    with open(file_name, 'r') as data:
        db = json.load(data)
    events = get_pn_vec_from_range_for_hosts(db2013)
    hosts = []
    host = 0
    for item in events[0].most_common(100):
        skip = False
        #print item
        if host > 1:
            break
        for i in item[0]:
            if i in IGNORE_WORDS:
                skip = True
                break
        if skip:
            continue
        if item[0][0] in map(lambda x: x.lower(), names.words()) or item[0][1] in map(lambda x: x.lower(), names.words()):
            hosts.append(' '.join(word for word in item[0]))
            host = host + 1
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    #pn_count_vec = [["none", 0]]
    winners_old = []
    db = db2013
    events = {}
    event_freq = {}

    propers = []
    
    for event_index in get_event_indicies(get_tpm_arr((db))):
        for n in range(500):
            e = db[event_index + n]
            if re.search(r'win(s)?(ner)?', e['text'], re.IGNORECASE) and re.search(r'best', e['text'], re.IGNORECASE):
                for proper in strip_propers(normalize_str(e['text']).split()):
                    propers.append(proper)
                    events[event_index] = proper

    for i in events:
        freq = FreqDist(events[i])
        event_freq[i] = freq

    winners_names = Counter() 
    for i in event_freq:
        for p in event_freq[i].most_common(15):
            if "Best" not in p[0]:
                continue
            item_split = p[0].split(" ")
            new_string = ''
            start = False     
            for cur in item_split:
                print cur
                if start:
                    if len(cur) == 0:
                        continue
                    if '!' in cur:
                        new_string = new_string +  ' ' + cur
                        new_string.replace("!", "")
                        break
                    if ':' in cur:
                        new_string = new_string +  ' ' + cur
                        new_string.replace(":", "")
                        break
                    if not cur[0].isupper() or ',' in cur or '\'s' in cur or '.' in cur or 'buy' in cur:
                        break
                    new_string = new_string +  ' ' + cur
                if cur == "Best":
                    new_string = 'Best'
                    start = True            
            if new_string != '':
                new_string.replace('!', '')
                new_string.replace(':', '')
                if (new_string, i) not in winners_names.keys():
                    winners_names[(new_string, i)] = 0
                winners_names[(new_string, i)] += p[1]

    for item in winners_names.most_common(50):
        if item[0][0] != "Best" and item[0][0] != "Best Buy":
            winners_old.append(item[0])
        else:
            continue            
        stop = False
        remove = None
        for win in winners_old:
            print win
            if stop:
                break
            #for cur in item[0].split(" "):
                #if "Best" in cur:
                    #continue
            if (len(item[0][0].split(" ")) > 1 and item[0][0].split(" ")[1] == '') or (len(item[0][0].split(" ")) > 2 and item[0][0].split(" ")[2] == ''):
                continue
            if (len(item[0][0].split(" ")) > 2 and item[0][0].split(" ")[1] in win[0]) or (len(item[0][0].split(" ")) > 2 and item[0][0].split(" ")[2] in win[0]):
                if len(item[0][0]) > len(win[0]):
                    remove = win
                    stop = True
                    break      
                else:
                    remove = item[0]
        if remove:
            winners_old.remove(remove) 


        #winners_old.append(item[0])  
    #winners = []          
    #for winner in winners_old:
        #winner_split = winner.split(' ')
        #for win in winner_split:    
            #if win not in winners

    return winners_old

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
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
    print len(awards)
    for award in reg: 
        print award
        award_str = []
        for f in db:
            e = f['text']
            if 'supporting' in award:
                if 'supporting' not in e.lower():
                    continue
            if 'best score' in e.lower():
                print e
            if re.search(reg[award],e.lower()):                    
                for proper in strip_propers(normalize_str(e).split()):
                    winners_list[award].append(proper.lower().replace('\'','\"').strip(' '))
                continue

    test_winners_list = {}
    for a in winners_list:
        freq = FreqDist(winners_list[a])
        winners_freq[a] = freq
        #winners[a] = [] 
        test_winners_list[a] = []
    
    for h in winners_freq:
        done = False
        print h
        for win in winners_freq[h].most_common(25):
            #if done:
                #break
            stop = False
            if 'the' == win[0].lower():
                continue
            for a in h.split(' '):   
                if done:
                    break           
                if a.lower() in win[0].lower():
                    break
                for ignore in IGNORE_WORDS:
                    if ignore in win[0].lower():
                        stop = True
                        break
                for w in win[0].split(" "):
                    for host in hosts:
                        if w.lower() in host.lower():
                            stop = True
                            break
                if 'song' in h or 'screenplay' in h or 'score' in h:
                    if win[0].count('\'') != 2 and win[0].count('\"') != 2:
                        break
                if 'actor' in h or 'actress' in h or 'director' in h:
                    if 'the' in win[0].lower():
                        break
                    if len(win[0].split(' ')) < 2:
                        break
                    #print win[0]
                    #print win[0].split(' ')
                    if win[0].split(' ')[0] not in names.words() and win[0].split(' ')[1] not in names.words():
                        break
                if stop:
                    break   
                if not done:
                    winners[h] = (win[0].strip("\"")) #win[0].strip('\'').strip('\"'))
                test_winners_list[h].append(win)
                done = True
                break

    print test_winners_list
    #for h in test_winners_list:
        #for t in test_winners_list[h]:
            #print h
            #print t
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    #presenters = {}
    file_name = 'gg%s.json' % year
    with open(file_name, 'r') as data:
        db = json.load(data)
    presenters = []
    awards = OFFICIAL_AWARDS
    winners = {}
    winners_list = {}
    winners_freq = {}
    hosts = get_hosts(year)
    reg = REGEX_AWARDS
    propers = []
    winn = get_winner(year)

    for award in awards:
        winners_list[award] = []
    print len(awards)
    for award in reg: 
        print award
        award_str = []
        for f in db:
            e = f['text']
            if 'supporting' in award:
                if 'supporting' not in e.lower():
                    continue
            if re.search(r'\spresent(s)?(er)?', e.lower()):                   
                if re.search(reg[award],e.lower()): 
                    for proper in strip_propers(normalize_str(e).split()):
                        winners_list[award].append(proper.lower().replace('\'','\"').strip(' '))
                    continue
        test_winners_list = {}
    for f in db:
        e = f['text']
        if re.search(r'\s(a)?present(s)?(er)?', e.lower()):
            for win in winn:
                if winn[win] in e.lower():
                    for proper in strip_propers(normalize_str(e).split()):
                        if winn[win] not in proper:
                            winners_list[win].append(proper.lower().replace('\'','\"').strip(' '))
    for a in winners_list:
        freq = FreqDist(winners_list[a])
        winners_freq[a] = freq
        winners[a] = [] 
        test_winners_list[a] = []
    
    for h in winners_freq:
        count = 0
        done = False
        print h
        if 'the' == win[0].lower():
            continue
        for win in winners_freq[h].most_common(25):
            #if done:
                #break
            stop = False
            if 'the' == win[0].lower():
                continue
            for a in h.split(' '):   
                if done:
                    break   
                if '\"' in win[0]:
                    continue       
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
                if len(win[0].split(' ')) < 2:
                    break
                #print win[0]
                print win[0].split(' ')
                if win[0].split(' ')[0] not in names.words() and win[0].split(' ')[1] not in names.words():
                    break
                if stop:
                    break   
                if not done:
                    winners[h].append(win[0])
                test_winners_list[h].append(win)
                count = count + 1
                if count >= 2:
                    done = True
                break

    for t in test_winners_list:
        print test_winners_list[t]
    return winners

def get_presentersa(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    #presenters = {}
    file_name = 'gg%s.json' % year
    with open(file_name, 'r') as data:
        db = json.load(data)
    presenters = []
    awards = OFFICIAL_AWARDS
    presenters = {}
    presenters_list = {}
    presenters_freq = {}
    hosts = get_hosts(year)
    reg = REGEX_AWARDS
    propers = []
    presenters_aggregate = []
    winners = get_winner(year)

    for award in awards:
        presenters_list[award] = []
    print len(awards)
    for award in reg: 
        print award
        award_str = []
        for f in db:
            e = f['text']
            if 'aziz ansari' in e.lower():
                print e
            if 'supporting' in award:
                if 'supporting' not in e.lower():
                    continue
            if re.search(r'\s(a)?present(s)?(er)?', e.lower()):
                if re.search(reg[award],e.lower()): 
                    for proper in strip_propers(normalize_str(e).split()):
                        presenters_list[award].append(proper.lower().replace('\'','\"').strip(' '))
                    continue
    for f in db:
        e = f['text']
        if re.search(r'\s(a)?present(s)?(er)?', e.lower()):
            for win in winners:
                if winners[win] in e.lower():
                    for proper in strip_propers(normalize_str(e).split()):
                        if winners[win] not in proper:
                            presenters_list[win].append(proper.lower().replace('\'','\"').strip(' '))

    test_winners_list = {}
    for a in presenters_list:
        freq = FreqDist(presenters_list[a])
        presenters_freq[a] = freq
        presenters[a] = [] 
        test_winners_list[a] = []
    
    for h in presenters_freq:
        count = 0
        done = False
        print h
        print presenters_freq[h].most_common(5)
        for win in presenters_freq[h].most_common(25):
            #if done:
                #break
            stop = False
            if 'the' == win[0].lower():
                continue
            for a in h.split(' '):
                #for pres in presenters_aggregate:
                    #if pres not in win[0].lower():
                        #break
                if done:
                    break    
                if '\"' in win[0]:
                    continue
                if a.lower() in win[0].lower():
                    break
                for ignore in IGNORE_WORDS:
                    if ignore in win[0].lower():
                        stop = True
                        break
                #for w in win[0].split(" "):
                for host in hosts:
                    if host in win[0]:
                        stop = True
                        break
                if len(win[0].split(' ')) < 2:
                    break
                if win[0].split(' ')[0] not in names.words() and win[0].split(' ')[1] not in names.words():
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

    for t in test_winners_list:
        print t
        print test_winners_list[t]
    return presenters




    events = []
    matches = -1
    pn_count_vec = []    
    bigram = []
    trigram = []
    bigram = [w for s in db if re.search(r'\spresent(s)?(er)?', s['text']) for w in bigrams([w.lower() for w in word_tokenize(s['text']) if w.isalnum()])]
    #bigram = [w for s in db if re.search(r'win(s)?(ner)?', s['text']) for w in bigrams([w.lower() for w in word_tokenize(s['text']) if w.isalnum()])]
    #for s in db:
        #if re.search(r'\spresent(s)?(er)?', s['text']):
            #for w in word_tokenize(s['text']):
                #bigram.append(w)
    trigram = [w for s in db if re.search(r'\spresent(s)?(er)?', s['text']) for w in trigrams([w.lower() for w in word_tokenize(s['text']) if w.isalnum()])]
    #trigram = [w for s in db if re.search(r'\swin(s)?(ner)?', s['text']) for w in trigrams([w.lower() for w in word_tokenize(s['text']) if w.isalnum()])]
        #bigram = bigrams(word_tokenize(content))
    name = bigram + trigram
    pn_count_vec = FreqDist(name)
        #pn_temp = FreqDist(names)

            #for variation in get_variations(item[0]):
                #if variation in pn_count_vec:
                    #pn_count_vec[item[0]] = pn_count_vec[item[0]] + pn_count_vec[variation]
    events.append(pn_count_vec)
        #j = j + 1
    for e in events:
        print e.most_common(200)
    for e in events:
        presenter = 0
        for item in e.most_common(2000):
            #print item
            #if presenter > 1:
                #break            
            if 'tina' not in item[0] and 'fey' not in item[0] and 'amy' not in item[0]:
                if item[0][0] in map(lambda x: x.lower(), names.words()) and item[0][1] in map(lambda x: x.lower(), names.words()):
                    if len(item[0]) < 3 or item[0][2] in map(lambda x: x.lower(), names.words()):
                        presenters.append(' '.join(word for word in item[0]))
                        print item
                        presenter = presenter + 1
        print presenters

    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print "Pre-ceremony processing complete."
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    #db = db2013
    # Your code here
    #events = get_pn_vec_from_range(db2013)
    #for e in events:
        #print e.most_common(50)
    #print get_hosts('2013')
    print get_presenters('2013')
    #print get_winner('2015')
    #print get_awards('2013')

    return

if __name__ == '__main__':
    main()
