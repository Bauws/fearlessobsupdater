import requests
from bs4 import BeautifulSoup


def pick_helper(url):
    url = url
    series_data = []
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        matches = [match for match in soup.find_all("a", class_="section-anchor") if
                   match.get("name", "").startswith("submatch-")]

        for match in matches:
            match_data = []
            team_1_picks = []
            team_2_picks = []
            match_name = match.get("name")

            section = match.find_parent("section")

            if section:

                picks = section.find_all("ul", class_="content-match-sub-picks")
                for i, pick_list in enumerate(picks):
                    for pick in pick_list.find_all("img"):
                        if i == 0:
                            champion = pick.get('title').replace("'", "").replace(" ", "").lower()
                            if champion:
                                team_1_picks.append(champion)
                        else:
                            champion = pick.get('title').replace("'", "").replace(" ", "").lower()
                            if champion:
                                team_2_picks.append(champion)

            # Only append if contains champions
            if team_1_picks:
                match_data.append(team_1_picks)
            if team_2_picks:
                match_data.append(team_2_picks)
            if match_data:
                series_data.append(match_data)
    else:
        print(f"Fehler: {response.status_code}")

    return series_data


def pick_helper_v2(url):

    match_data = {
        'team1': {},
        'team2': {}
    }

    response = requests.get(url)

    if response.status_code != 200:
        return {
            "status_code": response.status_code
        }

    soup = BeautifulSoup(response.text, 'html.parser')

    match_info = soup.find('div', class_='content-match-head')

    score = soup.find('span', class_='txt-score').text.split(':')
    match_data['team1']['score'] = score[0]
    match_data['team2']['score'] = score[1]

    team_names = match_info.find_all('h2')
    match_data['team1']['team_name_short'] = team_names[0].text
    match_data['team2']['team_name_short'] = team_names[1].text

    div_img_back = match_info.find_all('div', class_='img-back')

    match_data['team1']['team_name_long'] = div_img_back[0].find('img').get('alt', None)
    match_data['team1']['team_logo_url'] = div_img_back[0].find('img').get('src', None)

    match_data['team2']['team_name_long'] = div_img_back[1].find('img').get('alt', None)
    match_data['team2']['team_logo_url'] = div_img_back[1].find('img').get('src', None)

    lineups = soup.find_all('ul', class_='content-match-lineup')

    positions = ['top', 'jungle', 'mid', 'adc', 'support']

    team1_lineup = {position: player_name.text for position, player_name in
                    zip(positions, lineups[0].find_all('div', class_='txt-info content-match-lineup-nick'))}
    team2_lineup = {position: player_name.text for position, player_name in
                    zip(positions, lineups[1].find_all('div', class_='txt-info content-match-lineup-nick'))}

    match_data['team1']['team_lineup'] = team1_lineup
    match_data['team2']['team_lineup'] = team2_lineup

    team1_games = {}
    team2_games = {}

    matches = [match for match in soup.find_all("a", class_="section-anchor") if
               match.get("name", "").startswith("submatch-")]

    for match in matches:
        team1_picks = []
        team2_picks = []
        match_name = match.get("name", None)

        section = match.find_parent("section")
        if section:

            picks = section.find_all("ul", class_="content-match-sub-picks")

            for i, pick_list in enumerate(picks):
                for pick in pick_list.find_all("img"):
                    if i == 0:
                        champion = pick.get('title').replace("'", "").replace(" ", "").lower()
                        if champion:
                            team1_picks.append(champion)
                    else:
                        champion = pick.get('title').replace("'", "").replace(" ", "").lower()
                        if champion:
                            team2_picks.append(champion)
        if team1_picks:
            team1_games[match_name] = team1_picks
        if team2_picks:
            team2_games[match_name] = team2_picks

    match_data['team1']['games'] = team1_games
    match_data['team2']['games'] = team2_games

    return match_data


if __name__ == '__main__':
    print(pick_helper_v2('https://www.primeleague.gg/de/matches/591905-teamorangegaming-academy-vs-a-one-man-army'))
