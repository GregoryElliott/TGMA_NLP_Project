import gg_api
import json

with open('gg2015answers.json') as f:
	j = json.load(f)

mine = gg_api.get_winner(2015)

for award in mine:
	if j['award_data'][award]['winner'] != mine[award]:
		print 'award: ' + award
		print 'correct: ' + j['award_data'][award]['winner']
		print 'mine: ' + mine[award]
