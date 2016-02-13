import json
import time

    
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

TPM_THRESHOLD = 1100

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
    ns +=s[0].lower()
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


def get_pn_vec_from_range(db):
    def get_variations(s):
        base = s.split()
        variations = []
        for n in base:
            variations.append(n)
        variations.append(s)
        return variations
    pn_count_vec = [["none", 0]]
    event_index = get_event_indicies(get_tpm_arr((db)))[1]
    matches = -1
    for n in range(0,100):
        tweet_index = event_index + n
        for proper in strip_propers(normalize_str(db[tweet_index]['text']).split()):
            for variation in get_variations(proper):
                for i in range(0, len(pn_count_vec)):
                    if pn_count_vec[i][0].find(variation) != -1:
                        matches = i
                        break
            if (matches == -1):
                pn_count_vec.append([proper,0])
            else:
                pn_count_vec[matches][1] += 1
                matches = -1
    return pn_count_vec


#### ---------------------- API Accesing Functions ------------------------- ####
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
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

def get_winners(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
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
    return

if __name__ == '__main__':
    main()
