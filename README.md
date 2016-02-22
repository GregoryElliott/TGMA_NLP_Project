# GG Awards Parser
Greg Elliott, Matt George, Tim Sullivan, Athif Wulandana
### Overview
GG Awards Parser is a tweet parsing system that extracts information from a given json database of tweets. Using event logic, the parser classifies information pertaining to the awards, winners, presenters, hosts and nominees included within the database. 

### Bonus Features
Accessible via the Text Interface. Determine: 
* Who was the best dressed of the night
```sh
bestdress  [year]
```
* Who gave the best joke of night
```sh
bestjoke [year]
```

### External Dependencies
Before using GG Awards Parser, ensure that you have the following dependencies installed:

* [NLTK] - a toolkit for natural language processing


### Text Interface

To enter the text interface, navigate to where you installed GG Awards Parser and type:

```sh
$ python gg_api.py enter
```
Available Commands: 
```sh
hosts [year]      Displays the hosts for a given year
awards [year]     Displays the awards for a given year
nominees [year]   Displays the nominees for a given year
winners [year]    Displays the winners for a given year
presenters [year] Displays the presenters for a given year
bestdress [year]  Displays best dressed individual for a given year
bestjoke [year]   Displays who gave the best joke for a given year
help              Display all available commands
exit              Quit the program

```


   [NLTK]: <http://www.nltk.org>

