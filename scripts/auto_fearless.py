import obspython as obs
import os
from PIL import Image
from io import BytesIO
import requests

from scrapper import pick_helper, pick_helper_v2

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
image_directory = os.path.join(script_dir, "..", "icons", "champion")
teamlogo_directory = os.path.join(script_dir, "..", "icons", "team")
# match_url = ""  # Store the URL input


def script_description():
    return "Fearless Draft - Auto Update with URL & Headers"


def script_properties():
    # Adds a text field for the URL input in OBS
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "reset_overlay_button", "Reset Overlay", reset_overlay_button_callback)
    obs.obs_properties_add_text(props, "match_url", "Match URL", obs.OBS_TEXT_DEFAULT)
    combobox = obs.obs_properties_add_list(props, "side_selector", "Blue Side", obs.OBS_COMBO_TYPE_LIST,
                                           obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(combobox, "Team 1", "team1")
    obs.obs_property_list_add_string(combobox, "Team 2", "team2")
    return props


def reset_overlay_button_callback(pressed, prop):
    if pressed:
        reset_overlay()


def script_update(settings):
    # Called when the script settings are changed. Updates picks from the new URL
    blue_side = obs.obs_data_get_string(settings, "side_selector")
    match_url = obs.obs_data_get_string(settings, "match_url")
    reset_overlay()
    fetch_and_update_picks(blue_side, match_url)


def script_load(settings):
    # Called when the script is loaded. Fetches data from pick_helper() and updates OBS sources
    print("Fearless Draft script loaded.")
    fetch_and_update_picks()


def reset_overlay():
    # Clears all champion images and headers to reset OBS overlay
    print("Resetting overlay: Clearing all images and headers.")
    clear_all_picks()
    clear_all_headers()


def fetch_and_update_picks(blue_side=None, match_url=None):

    if not match_url:
        print("No URL provided. Waiting for input...")
        return

    print(f"Fetching picks from v2: {match_url}")
    data = pick_helper_v2(match_url)

    if not data:
        print("No picks received. Clearing all sources...")
        reset_overlay()
        return

    if blue_side == "team1":
        side_team1 = "Blue"
        side_team2 = "Red"
    else:
        side_team1 = "Red"
        side_team2 = "Blue"

    # Team 1 - Data

    team1 = data["team1"]

    team1_score = team1["score"]

    update_text_source(f"Score Team {side_team1}", team1_score)

    team1_short_name = team1["team_name_short"]
    team1_logo_url = team1["team_logo_url"]

    response = requests.get(team1_logo_url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        target_height = 200
        width_percent = target_height / float(image.height)
        target_width = int(image.width * width_percent)
        resized_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        os.makedirs(teamlogo_directory, exist_ok=True)
        logo_path = os.path.join(teamlogo_directory, f"{team1_short_name}.png")
        resized_image.save(logo_path)
        print("Image downloaded and resized successfully!")
        update_image_source(f"Team Logo {side_team1}", logo_path)
    else:
        print("Failed to download image. Status code:", response.status_code)

    games = team1["games"]

    for key in games:
        game_number = key.replace("submatch", "").replace("-", "")

        update_text_source(f"Game {game_number} Header {side_team1}", f"Game {game_number}")

        picks = games[key]

        for i, champ in enumerate(picks):
            icon_path = os.path.join(image_directory, f"{champ}.png")
            update_image_source(f"Game {game_number} {side_team1} Pick {i + 1}", icon_path)

    # Team 2 - Data

    team2 = data["team2"]

    team2_score = team2["score"]

    update_text_source(f"Score Team {side_team2}", team2_score)

    team2_short_name = team2["team_name_short"]
    team2_logo_url = team2["team_logo_url"]

    response = requests.get(team2_logo_url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        target_height = 200
        width_percent = target_height / float(image.height)
        target_width = int(image.width * width_percent)
        resized_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        os.makedirs(teamlogo_directory, exist_ok=True)
        logo_path = os.path.join(teamlogo_directory, f"{team2_short_name}.png")
        resized_image.save(logo_path)
        print("Image downloaded and resized successfully!")
        update_image_source(f"Team Logo {side_team2}", logo_path)
    else:
        print("Failed to download image. Status code:", response.status_code)

    games = team2["games"]

    for key in games:
        game_number = key.replace("submatch", "").replace("-", "")

        update_text_source(f"Game {game_number} Header {side_team2}", f"Game {game_number}")

        picks = games[key]

        # Update team 2 picks
        for i, champ in enumerate(picks):
            icon_path = os.path.join(image_directory, f"{champ}.png")
            update_image_source(f"Game {game_number} {side_team2} Pick {i + 1}", icon_path)


def clear_all_picks():
    # Removes all champion images from OBS
    for game_number in range(5):
        for i in range(5):
            hide_image_source(f"Game {game_number + 1} Blue Pick {i + 1}")
            hide_image_source(f"Game {game_number + 1} Red Pick {i + 1}")


def clear_all_headers():
    # Clears all game headers
    for game_number in range(5):
        update_text_source(f"Game {game_number + 1} Header Blue", "")
        update_text_source(f"Game {game_number + 1} Header Red", "")


def update_image_source(image_source_name, path):
    # Updates an image source only if the image file exists
    source = obs.obs_get_source_by_name(image_source_name)

    if not source:
        print(f"Image source {image_source_name} not found!")
        return

    # Check if the image file exists
    if os.path.exists(path):
        update_image(source, path)
    else:
        hide_image(source)

    obs.obs_source_release(source)


def hide_image_source(image_source_name):
    # Hides an image source by setting an empty file
    source = obs.obs_get_source_by_name(image_source_name)

    if not source:
        print(f"Image source {image_source_name} not found!")
        return

    hide_image(source)
    obs.obs_source_release(source)


def update_text_source(text_source_name, text_value):
    # Updates a text source in OBS
    source = obs.obs_get_source_by_name(text_source_name)

    if not source:
        print(f"Text source {text_source_name} not found!")
        return

    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", text_value)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)


def update_image(source, icon_path):
    # Sets an image source to display the given file
    image_settings = obs.obs_data_create()
    obs.obs_data_set_string(image_settings, "file", icon_path)
    obs.obs_source_update(source, image_settings)
    obs.obs_data_release(image_settings)


def hide_image(source):
    # Hides an image source by setting an empty file
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "file", "")
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
