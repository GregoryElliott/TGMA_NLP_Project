
### Word-Vector
### (Utility)
########################################################################

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
