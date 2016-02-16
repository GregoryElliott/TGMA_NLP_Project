import json
import time
import nltk
from nltk.book import FreqDist
from nltk.corpus import names
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import trigrams
from nltk.tokenize import *
import re

    
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
    ns += s[0].lower()
    for i in range(1, len(s)):
        ns += s[i]

    return ns


def strip_propers(s):
    '''Returns a list proper nouns from a list-of Tokens'''
    proper_nouns = []
    noun_group = ""
    for token in s:
        if (token[0].isupper()):
            noun_group += token + " "
        else:
            if(noun_group == ""): continue
            else:
                proper_nouns.append(noun_group)
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


#### ---------------------- API Accesing Functions ------------------------- ####
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    db = 'db' + year
    events = get_pn_vec_from_range(db2013)
    hosts = []
    host = 0
    print events[0].most_common(100)
    for item in events[0].most_common(100):
        #print item
        if host > 1:
            break            
        if item[0][0] in map(lambda x: x.lower(), names.words()) or item[0][1] in map(lambda x: x.lower(), names.words()):
            hosts.append(' '.join(word for word in item[0]))
            print item
            host = host + 1
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winnersa(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    #db = 'db' + year
    db = db2013
    events = []
    winners = []


    #for event_index in get_event_indicies(get_tpm_arr((db))):
        #pn_count_vec = []
        #for n in range(500):
            #for s in db[event_index + n]:
                #if re.search(r'win(s)?(ner)?', s['text']):
                    #for w in bigrams([w.lower() for w in word_tokenize(s['text']) if w.isalnum()]):
                        #return
        #bigram = [w for n in range(300) for s in sent_tokenize(db[event_index + n]['text']) if re.search(r'win(s)?(ner)?', s, re.IGNORECASE) and re.search(r'best', s, re.IGNORECASE) for w in bigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
    bigram = [w for s in db if re.search(r'win(s)?(ner)?', s['text'], re.IGNORECASE) and re.search(r'best', s['text'], re.IGNORECASE) for w in bigrams([w for w in word_tokenize(s['text'])]) if w[0][0].isupper() and w[1][0].isupper()]
        #trigram = [w for n in range(300) for s in sent_tokenize(db[event_index + n]['text']) if re.search(r'win(s)?(ner)?', s, re.IGNORECASE) and re.search(r'best', s, re.IGNORECASE) for w in trigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
    trigram = [w for s in db if re.search(r'win(s)?(ner)?', s['text'], re.IGNORECASE) and re.search(r'best', s['text'], re.IGNORECASE) for w in trigrams([w for w in word_tokenize(s['text'])]) if w[0][0].isupper() and w[1][0].isupper() and w[2][0].isupper()]
    name = bigram + trigram
    pn_count_vec = FreqDist(name)
    events.append(pn_count_vec)

    for e in events:
        winner = 0
        for item in e.most_common(1000):
            print item
            #print item
            #if winner > 5:
                #break      
            if 'tina' not in item[0] and 'fey' not in item[0] and 'amy' not in item[0]:      
                if item[0][0].lower() in map(lambda x: x.lower(), names.words()) and item[0][1].lower() in map(lambda x: x.lower(), names.words()):
                    if len(item[0]) < 3 or item[0][2].lower() in map(lambda x: x.lower(), names.words()):
                        winners.append(' '.join(word for word in item[0]))
                        print item
                        winner = winner + 1
    return winners

def get_winners(year):
    #pn_count_vec = [["none", 0]]
    winners = []
    db = db2013
    events = []

    for event_index in get_event_indicies(get_tpm_arr((db))):
        pn_count_vec = []
        #for n in range(500):
            #for s in db[event_index + n]:
                #if re.search(r'win(s)?(ner)?', s['text']):
                    #for w in bigrams([w.lower() for w in word_tokenize(s['text']) if w.isalnum()]):
                        #return
        bigram = [proper for n in range(500) for proper in strip_propers(normalize_str(db[event_index+n]['text']).split()) if re.search(r'win(s)?(ner)?', db[event_index+n]['text'], re.IGNORECASE) and re.search(r'best', db[event_index+n]['text'], re.IGNORECASE)]

    #bigram = [w for s in db if re.search(r'win(s)?(ner)?', s['text'], re.IGNORECASE) and re.search(r'best', s['text'], re.IGNORECASE) for w in bigrams([w for w in word_tokenize(s['text'])]) if w[0][0].isupper() and w[1][0].isupper()]
        #trigram = [w for n in range(300) for s in sent_tokenize(db[event_index + n]['text']) if re.search(r'win(s)?(ner)?', s, re.IGNORECASE) and re.search(r'best', s, re.IGNORECASE) for w in trigrams([w.lower() for w in word_tokenize(s) if w.isalnum()])]
    #trigram = [w for s in db if re.search(r'win(s)?(ner)?', s['text'], re.IGNORECASE) and re.search(r'best', s['text'], re.IGNORECASE) for w in trigrams([w for w in word_tokenize(s['text'])]) if w[0][0].isupper() and w[1][0].isupper() and w[2][0].isupper()]
        name = bigram #+ trigram
        pn_count_vec = FreqDist(name)
        events.append(pn_count_vec)

    for e in events:
        winner = 0
        print e.most_common(100)
        for item in e.most_common(100):
            #print item
            #if winner > 5:
                #break      
            #if 'tina' not in item[0] and 'fey' not in item[0] and 'amy' not in item[0]:      
                #if item[0][0].lower() in map(lambda x: x.lower(), names.words()) and item[0][1].lower() in map(lambda x: x.lower(), names.words()):
                    #if len(item[0]) < 3 or item[0][2].lower() in map(lambda x: x.lower(), names.words()):
            for w in item[1]:
                if not w[0].isupper():
                    continue
            winners.append(' '.join(word for word in item[0]))
            print item
            winner = winner + 1
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    #presenters = {}
    presenters = []
    db = db2013

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


    #for event_index in get_event_indicies(get_tpm_arr((db))):
        #if j > 6:
            #break
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
    # Your code here
    #events = get_pn_vec_from_range(db2013)
    #for e in events:
        #print e.most_common(50)
    #print get_hosts('2013')
    #print get_presenters('2013')
    print get_winners('2013')
    #for e in db2013:
        #if "Bradley" in e['text'] or "Cooper" in e['text']:
        #if re.search(r'win(s)?(ner)?', e['text']):
        #if 'present' in e['text']:
            #print e['text']
    return

if __name__ == '__main__':
    main()
