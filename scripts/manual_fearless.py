import obspython as obs
import os

picks_team_1 = [[""] * 5 for _ in range(5)]
picks_team_2 = [[""] * 5 for _ in range(5)]
headers_team_1 = [""] * 5
headers_team_2 = [""] * 5

previous_picks_team_1 = [[""] * 5 for _ in range(5)]
previous_picks_team_2 = [[""] * 5 for _ in range(5)]
previous_headers_team_1 = [""] * 5
previous_headers_team_2 = [""] * 5

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
image_directory = os.path.join(script_dir, "..", "icons", "champion")


def script_description():
    return "Fearless Draft - Optimized"


def script_properties():
    props = obs.obs_properties_create()

    for game_number in range(5):
        # Blue Team Header
        obs.obs_properties_add_text(props, f"blue_header_{game_number + 1}", f"Game {game_number + 1} Blue Team Title", obs.OBS_TEXT_DEFAULT)
        for blue_team in range(5):
            obs.obs_properties_add_text(props, f"game_{game_number + 1}_blue_pick_{blue_team + 1}", f"Blue {blue_team + 1}", obs.OBS_TEXT_DEFAULT)

        # Red Team Header
        obs.obs_properties_add_text(props, f"red_header_{game_number + 1}", f"Game {game_number + 1} Red Team Title", obs.OBS_TEXT_DEFAULT)
        for red_team in range(5):
            obs.obs_properties_add_text(props, f"game_{game_number + 1}_red_pick_{red_team + 1}", f"Red {red_team + 1}", obs.OBS_TEXT_DEFAULT)

    return props


def script_update(settings):
    global picks_team_1, picks_team_2, headers_team_1, headers_team_2
    global previous_picks_team_1, previous_picks_team_2, previous_headers_team_1, previous_headers_team_2

    # Track if updates are needed
    updated = False

    for game_number in range(5):
        # Check and update headers
        new_header_1 = obs.obs_data_get_string(settings, f"blue_header_{game_number + 1}")
        new_header_2 = obs.obs_data_get_string(settings, f"red_header_{game_number + 1}")

        if new_header_1 != previous_headers_team_1[game_number]:
            previous_headers_team_1[game_number] = new_header_1
            update_text_source(f"blue_header_{game_number + 1}", new_header_1)
            updated = True

        if new_header_2 != previous_headers_team_2[game_number]:
            previous_headers_team_2[game_number] = new_header_2
            update_text_source(f"red_header_{game_number + 1}", new_header_2)
            updated = True

        # Check and update picks
        for blue_team in range(5):
            new_pick = obs.obs_data_get_string(settings, f"game_{game_number + 1}_blue_pick_{blue_team + 1}").lower().replace("'", "").replace(" ", "")
            if new_pick != previous_picks_team_1[game_number][blue_team]:
                previous_picks_team_1[game_number][blue_team] = new_pick
                update_image_source(f"game_{game_number + 1}_blue_pick_{blue_team + 1}_image", new_pick)
                updated = True

        for red_team in range(5):
            new_pick = obs.obs_data_get_string(settings, f"game_{game_number + 1}_red_pick_{red_team + 1}").lower().replace("'", "").replace(" ", "")
            if new_pick != previous_picks_team_2[game_number][red_team]:
                previous_picks_team_2[game_number][red_team] = new_pick
                update_image_source(f"game_{game_number + 1}_red_pick_{red_team + 1}_image", new_pick)
                updated = True

    if updated:
        print("Overlay updated.")


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


def script_load(settings):
    print("Fearless Draft script loaded.")
