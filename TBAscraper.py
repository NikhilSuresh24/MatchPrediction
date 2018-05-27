# ALL TBA SCRAPING
import tbapy
import numpy as np
from tqdm import tqdm


def scrape_match(tba_key: str, year : int, event_name : str, match_num : int, match_type='qm', round=None):
	tba = tbapy.TBA(TBA_KEY)
	event_key = ''
	red_data = []
	blue_data = []

	for event in tba.events(year):
		if event.name == event_name:
			event_key = event.key
			break

	red_alliance_teams = tba.match(year=year, event=event_key, type=match_type, number=match_num)['alliances']['red']['team_keys'] if match_type=='qm' else tba.match(year=year, event=event_key, type=match_type, number=match_num, round=round)['alliances']['red']['team_keys']
	blue_alliance_teams = tba.match(year=year, event=event_key, type=match_type, number=match_num)['alliances']['blue']['team_keys'] if match_type=='qm' else tba.match(year=year, event=event_key, type=match_type, number=match_num, round=round)['alliances']['blue']['team_keys']
	
	for team in red_alliance_teams:
		team_data = tba.team_status(team, event_key)['qual']['ranking']['sort_orders']
		red_data.append(team_data)
	for team in blue_alliance_teams:
		team_data = tba.team_status(team, event_key)['qual']['ranking']['sort_orders']
		blue_data.append(team_data)

	return red_data, blue_data

def make_dataset(tba_key : str, year : int, saveFile : str):
	tba = tbapy.TBA(TBA_KEY)
	x = []
	Y = []
	for event in tqdm(tba.events(year)):
		event_key = event.key
		for match in tqdm(tba.event_matches(event_key)):
			red_alliance = match['alliances']['red']['team_keys']            
			blue_alliance = match['alliances']['blue']['team_keys']
			red_score = match['alliances']['red']['score']
			blue_score = match['alliances']['blue']['score']

			try:            
				red_data = [tba.team_status(team, event_key)['qual']['ranking']['sort_orders'] for team in red_alliance]
				blue_data =[tba.team_status(team, event_key)['qual']['ranking']['sort_orders'] for team in blue_alliance]	
				red_data = red_data[0] + red_data[1] + red_data[2]
				blue_data = blue_data[0] + blue_data[1] + blue_data[2]
			except:
				continue

			x.append(red_data + blue_data)
			x.append(blue_data + red_data)
			Y.append(red_score)
			Y.append(blue_score)

	np.savez(saveFile, x=np.array(x), y=np.array(Y))

TBA_KEY = "pfAELfi9W9zr4ONbwppQMNFmeaQbOMjeTo6liUiDlJSJGcvUYxIWXF5C4zdJxHYT"
year = 2018
saveFile = "matchData.npy"

make_dataset(TBA_KEY, year, saveFile)