import tbapy
TBA_KEY = "pfAELfi9W9zr4ONbwppQMNFmeaQbOMjeTo6liUiDlJSJGcvUYxIWXF5C4zdJxHYT"


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


red, blue = scrape_match(TBA_KEY, 2017, "Silicon Valley Regional", 2, 'sf', 1)
print(red)
