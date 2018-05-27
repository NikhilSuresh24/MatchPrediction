# ALL TBA SCRAPING
import tbapy
import numpy as np
from tqdm import tqdm
import sys

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def scrape_match(tba_key: str, year : int, event_name : str, match_num : int, match_type='qm', round=False):
	'''Given TBA-Authentication key, Competition year, event name, and match number, queries TBA for basic match data of each team in the match.'''
	tba = tbapy.TBA(tba_key)
	year = int(year)
	match_num = int(match_num)
	round = int(round)
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

def inference(red_data, blue_data):
	'''Given data on red and blue alliance, returns predicted score for each alliance'''
	net = torch.load('netweights.pt')
	data1 = Variable(torch.FloatTensor(red_data[0] + red_data[1] + red_data[2] + blue_data[0] + blue_data[1] + blue_data[2]))
	data2 = Variable(torch.FloatTensor(blue_data[0] + blue_data[1] + blue_data[2] + red_data[0] + red_data[1] + red_data[2]))
	red_score = net(data1)
	blue_score = net(data2)
	print(red_score, blue_score)

TBA_KEY = "pfAELfi9W9zr4ONbwppQMNFmeaQbOMjeTo6liUiDlJSJGcvUYxIWXF5C4zdJxHYT"

red_data, blue_data = scrape_match(TBA_KEY, year=sys.argv[1], event_name=sys.argv[2], match_num=sys.argv[3], match_type=sys.argv[4], round=sys.argv[5])
inference(red_data, blue_data)

