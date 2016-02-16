#import json
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

# Not if this is how you file dependencies in python...
from constants import *
from awards_parse import *
from events import *


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
    for token in s:
        if (token[0].isupper()) or token[0] == '\'' or token[0] == '\"':
            noun_group += token + " "
            if token[len(token) - 1] == '\'' or token[len(token) - 1] == '\"':
                proper_nouns.append(noun_group)
                noun_group = ""
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


def get_winners(year):
    #pn_count_vec = [["none", 0]]
    #awards = get_awards(2013)
    #awards = [u'best performance by an actress in a supporting role in a motion picture', u'best performance by an actor in a mini-series or motion picture made for television', u'best director - motion picture', u'best original song - motion picture', u'best performance by an actor in a motion picture - comedy or musical', u'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television', u'best performance by an actress in a motion picture - comedy or musical', u'cecil b. demille award', u'best performance by an actress in a mini-series or motion picture made for television', u'best animated feature film', u'best motion picture - drama', u'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', u'best performance by an actor in a television series - drama', u'best performance by an actress in a motion picture - drama', u'best screenplay - motion picture', u'best original score - motion picture', u'best foreign language film', u'best performance by an actor in a supporting role in a motion picture', u'best motion picture - comedy or musical', u'best mini-series or motion picture made for television', u'best television series - drama', u'best performance by an actress in a television series - comedy or musical', u'best television series - comedy or musical', u'best performance by an actor in a motion picture - drama', u'best performance by an actress in a television series - drama', u'best performance by an actor in a television series - comedy or musical']
    awards = [u'best supporting actress', u'best actor mini-series television', u'best director', u'best original song', u'best actor', u'best supporting actor television', u'best actress', u'cecil b. demille award', u'best actress television', u'best animated feature film', u'best drama', u'best supporting actress television', u'best actor television drama', u'best actress drama', u'best screenplay', u'best original score', u'best foreign language film', u'best supporting actor', u'best motion picture comedy or musical', u'best mini-series or motion picture made for television', u'best television series drama', u'best actress television series comedy or musical', u'best television series comedy or musical', u'best actor drama', u'best actress drama', u'best actor comedy or musical']
    winners_old = []
    db = db2013
    winners = {}
    winners_list = {}
    winners_freq = {}
    events = []

    propers = []

    # for e in db:    
    #     if re.search(r'win(s)?(ner)?', e['text'], re.IGNORECASE) and re.search(r'best', e['text'], re.IGNORECASE):
    #         for proper in strip_propers(normalize_str(e['text']).split()):
    #             propers.append(proper)


    for award in awards:
        winners_list[award] = []
    print len(awards)
    for award in awards: 
        print award
        for e in db:
            if "RT" not in e['text']:
                continue
            count = 0
            for a in award.split(" "):
                if a in e['text']:
                    count = count + 1
                if count > 1:
                    for proper in strip_propers(normalize_str(e['text']).split()):
                        #propers.append(proper)
                        p = proper.strip(' ')                        
                        winners_list[award].append(p)
                    continue

    for a in winners_list:
        freq = FreqDist(winners_list[a])
        winners_freq[a] = freq
    
    for h in winners_freq:
        print h
        for win in winners_freq[h].most_common(20):
            for a in h.split(' '):
                if a in win:
                    continue
                if "RT" in win:
                    continue
                winners[h] = win
                break
    return winners

    events.append(freq)

    winners_names = Counter()
    for p in events[0].most_common(1000):
        item_split = p[0].split(" ")
        new_string = ''
        for cur in item_split:
            if cur in names.words():
                new_string = new_string + cur + ' '
        if new_string != '':
            if new_string not in winners_names.keys():
                winners_names[new_string] = 0
            winners_names[new_string] += p[1]

    for e in events:
        presenter = 0
        for item in e.most_common(300):
            #print item
            #if presenter > 1:
                #break  
            item_split = item[0].split(" ")   
            print item_split            
            if '\'' in item[0] or '\"' in item[0]:
                winners_old.append(item[0])
                add = True
                for cur in winners_old:
                    for spl in item_split:
                        if spl in cur:
                            add = False
                if add:
                    winners_old.append(item[0])
                    presenter = presenter + 1
    for item in winners_names.most_common(40):
        print item
        if 'tina' not in item[0] and 'fey' not in item[0] and 'amy' not in item[0]:
            winners_old.append(item[0])  
    #winners = []          
    #for winner in winners_old:
        #winner_split = winner.split(' ')
        #for win in winner_split:    
            #if win not in winners

    return winners_old

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
    db = db2013
    # Your code here
    #events = get_pn_vec_from_range(db2013)
    #for e in events:
        #print e.most_common(50)
    #print get_hosts('2013')
    #print get_presenters('2013')
    #print get_winners('2013')
    print get_awards('2013')
    return

if __name__ == '__main__':
    main()



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

def get_winnersa(year):
    #pn_count_vec = [["none", 0]]
    winners = []
    db = db2013
    events = []

    #for event_index in get_event_indicies(get_tpm_arr((db))):
        #pn_count_vec = []
        #for n in range(500):
            #for s in db[event_index + n]:
                #if re.search(r'win(s)?(ner)?', s['text']):
                    #for w in bigrams([w.lower() for w in word_tokenize(s['text']) if w.isalnum()]):
                        #return
        #bigram = [proper for n in range(500) for proper in strip_propers(normalize_str(db[event_index+n]['text']).split()) if re.search(r'win(s)?(ner)?', db[event_index+n]['text'], re.IGNORECASE) and re.search(r'best', db[event_index+n]['text'], re.IGNORECASE)]
        #bigram = [proper for n in range(500) for proper in strip_propers(normalize_str(db[event_index+n]['text']).split()) if re.search(r'best', db[event_index+n]['text'], re.IGNORECASE)]        
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
        #bigram = [proper for n in range(500) for proper in strip_propers(normalize_str(db[event_index+n]['text']).split()) if re.search(r'win(s)?(ner)?', db[event_index+n]['text'], re.IGNORECASE) and re.search(r'best', db[event_index+n]['text'], re.IGNORECASE)]
    bigram = [proper for e in db for proper in strip_propers(normalize_str(e['text']).split()) if re.search(r'best', db[event_index+n]['text'], re.IGNORECASE)]        

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
            skip = False
            for w in word_tokenize(item[0]):
                print w
                print w[0]
                if not w[0].isupper():
                    skip = True
            if not skip:
                winners.append(' '.join(word for word in item[0]))
                print item
                winner = winner + 1
    return winners


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
            skip = False
            for w in word_tokenize(item[0]):
                print w
                print w[0]
                if not w[0].isupper():
                    skip = True
            if not skip:
                winners.append(' '.join(word for word in item[0]))
                print item
                winner = winner + 1
    return winners


def get_awardsa(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    #pn_count_vec = [["none", 0]]
    winners_old = []
    db = db2013
    #events = {}
    events = []

    propers = []
    
    for e in db:
        if re.search(r'win(s)?(ner)?', e['text'], re.IGNORECASE) and re.search(r'best', e['text'], re.IGNORECASE):
            for proper in strip_propers(normalize_str(e['text']).split()):
                propers.append(proper)

    freq = FreqDist(propers)
    events.append(freq)

    winners_names = Counter()
    for p in events[0].most_common(1000):
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
            if new_string not in winners_names.keys():
                winners_names[new_string] = 0
            winners_names[new_string] += p[1]

    for item in winners_names.most_common(50):
        if item[0] != "Best" and item[0] != "Best Buy":
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
            if (len(item[0].split(" ")) > 1 and item[0].split(" ")[1] == '') or (len(item[0].split(" ")) > 2 and item[0].split(" ")[2] == ''):
                continue
            if (len(item[0].split(" ")) > 2 and item[0].split(" ")[1] in win) or (len(item[0].split(" ")) > 2 and item[0].split(" ")[2] in win):
                if len(item[0]) > len(win):
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
