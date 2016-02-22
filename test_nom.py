import gg_api
import json

with open('gg2013answers.json') as f:
	j = json.load(f)

mine = gg_api.get_nominees(2013)

for award in mine:
	if j['award_data'][award]['nominees'] != mine[award]:
		print 'award: ' + award
		print 'correct: ' + str(j['award_data'][award]['nominees'])
		print 'mine: ' + str(mine[award])
