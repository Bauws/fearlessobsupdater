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
                teams = section.find_all("a", class_="content-match-sub-team-img")

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
