import gg_api
import json

with open('gg2013answers.json') as f:
	j = json.load(f)

mine = gg_api.get_presenters(2013)

for award in mine:
	if j['award_data'][award]['winner'] != mine[award]:
		print 'award: ' + award
		print 'correct: ' + str(j['award_data'][award]['presenters'])
		print 'mine: ' + str(mine[award])
