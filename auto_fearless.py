import obspython as obs
import os
from scrapper import pick_helper

picks_team_1 = [[""] * 5 for _ in range(5)]
picks_team_2 = [[""] * 5 for _ in range(5)]

image_directory = "C:/Users/lukas/PycharmProjects/ChampSelect/Icons/champion/"
pick_url = ""  # Store the URL input


def script_description():
    return "Fearless Draft - Auto Update with URL & Headers"


def script_properties():
    # Adds a text field for the URL input in OBS
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "pick_url", "Pick Helper URL", obs.OBS_TEXT_DEFAULT)
    return props


def script_update(settings):
    # Called when the script settings are changed. Updates picks from the new URL
    global pick_url
    new_url = obs.obs_data_get_string(settings, "pick_url")

    if new_url and new_url != pick_url:
        pick_url = new_url
        print(f"New URL detected: {pick_url}")
        reset_overlay()  # Clear all existing data before fetching new picks
        fetch_and_update_picks()


def script_load(settings):
    # Called when the script is loaded. Fetches data from pick_helper() and updates OBS sources
    print("Fearless Draft script loaded.")
    fetch_and_update_picks()


def reset_overlay():
    # Clears all champion images and headers to reset OBS overlay
    print("Resetting overlay: Clearing all images and headers.")
    clear_all_picks()
    clear_all_headers()


def fetch_and_update_picks():
    # Fetches pick data from the provided URL and updates OBS sources
    if not pick_url:
        print("No URL provided. Waiting for input...")
        return

    print(f"Fetching picks from: {pick_url}")
    data = pick_helper(pick_url)

    # If data is empty, remove all icons and headers
    if not data:
        print("No picks received. Clearing all sources...")
        reset_overlay()
        return

    # Track if we need to update OBS
    updated = False

    for game_number, game_data in enumerate(data):
        if not isinstance(game_data, list) or len(game_data) != 2:
            print(f"Error: Invalid structure in game {game_number + 1}")
            continue

        team_1_picks, team_2_picks = game_data

        if len(team_1_picks) != 5 or len(team_2_picks) != 5:
            print(f"Error: Incorrect number of picks in game {game_number + 1}")
            continue

        # Update Headers
        update_text_source(f"blue_header_{game_number + 1}", f"Game {game_number + 1}")
        update_text_source(f"red_header_{game_number + 1}", f"Game {game_number + 1}")

        # Update team 1 picks
        for i, champ in enumerate(team_1_picks):
            if picks_team_1[game_number][i] != champ:
                picks_team_1[game_number][i] = champ
                update_image_source(f"game_{game_number + 1}_blue_pick_{i + 1}_image", champ)
                updated = True

        # Update team 2 picks
        for i, champ in enumerate(team_2_picks):
            if picks_team_2[game_number][i] != champ:
                picks_team_2[game_number][i] = champ
                update_image_source(f"game_{game_number + 1}_red_pick_{i + 1}_image", champ)
                updated = True

    if updated:
        print("Overlay updated with new picks and headers.")


def clear_all_picks():
    # Removes all champion images from OBS
    for game_number in range(5):
        for i in range(5):
            hide_image_source(f"game_{game_number + 1}_blue_pick_{i + 1}_image")
            hide_image_source(f"game_{game_number + 1}_red_pick_{i + 1}_image")


def clear_all_headers():
    # Clears all game headers
    for game_number in range(5):
        update_text_source(f"blue_header_{game_number + 1}", "")
        update_text_source(f"red_header_{game_number + 1}", "")


def update_image_source(image_source_name, champion_name):
    # Updates an image source only if the image file exists
    source = obs.obs_get_source_by_name(image_source_name)

    if not source:
        print(f"Image source {image_source_name} not found!")
        return

    # Check if the image file exists
    icon_path = os.path.join(image_directory, f"{champion_name}.png")
    if os.path.exists(icon_path):
        update_image(source, icon_path)
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
