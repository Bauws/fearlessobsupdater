import obspython as obs
import json
import os

def script_load(settings):
    # Get the current scene in OBS
    scene = obs.obs_frontend_get_current_scene()
    scene_source = obs.obs_scene_from_source(scene)

    json_path = os.path.join(os.path.dirname(__file__), "sources.json")

    # Load the JSON from the "sources.json" file
    try:
        with open(json_path, "r") as file:
            sources_data = json.load(file)
    except FileNotFoundError:
        obs.script_log(obs.LOG_ERROR, "File not found: %s", json_path)
        return
    except json.JSONDecodeError:
        obs.script_log(obs.LOG_ERROR, "Invalid JSON in file: %s", json_path)
        return

    # Loop over the sources data and create each source
    for source_data in sources_data:
        source_name = source_data["name"]
        source_type = source_data["type"]

        # Check if the source already exists
        existing_source = obs.obs_get_source_by_name(source_name)
        if existing_source:
            obs.script_log(obs.LOG_WARNING, f"Source '{source_name}' already exists. Skipping creation.")
            obs.obs_source_release(existing_source)
            continue

        if source_type == "text_gdiplus":
            # Create source settings directly from the JSON for the source
            source_settings = obs.obs_data_create()

            # Set text and font size
            obs.obs_data_set_string(source_settings, "text", source_data["text"])
            obs.obs_data_set_int(source_settings, "font_size", source_data["font_size"])

            # Create font settings (face, style, etc.)
            font_settings = obs.obs_data_create()
            obs.obs_data_set_string(font_settings, "face", "Arial")  # Set font face
            obs.obs_data_set_int(font_settings, "size", source_data["font_size"])  # Font size
            obs.obs_data_set_int(font_settings, "style", 0)  # Style: Regular (no bold/italic)

            # Add font settings to source settings
            obs.obs_data_set_obj(source_settings, "font", font_settings)

            # Create the source using the settings
            source = obs.obs_source_create(source_type, source_name, source_settings, None)

            # Add the source to the scene
            obs.obs_scene_add(scene_source, source)

        elif source_type == "image_source":
            # Create source settings directly from the JSON for the source
            source_settings = obs.obs_data_create()

            if "Logo" in source_data["name"]:
                path = os.path.join(os.path.dirname(__file__), f'../icons/team/{source_data["file"]}')
            else:
                path = os.path.join(os.path.dirname(__file__), f'../icons/champion/{source_data["file"]}')

            if not os.path.isfile(path):
                obs.script_log(obs.LOG_WARNING, f"Image file not found: {path}")
                continue

            obs.obs_data_set_string(source_settings, "file", path)
            obs.obs_data_set_int(source_settings, "width", 50)
            obs.obs_data_set_int(source_settings, "height", 50)

            # Create the source using the settings
            source = obs.obs_source_create(source_type, source_name, source_settings, None)

            # Add the source to the scene
            obs.obs_scene_add(scene_source, source)

            # Wait until the source is available in the scene
            scene_item = obs.obs_scene_find_source(scene_source, source_name)
            if scene_item:
                # Get the actual image source from the scene item
                item_source = obs.obs_sceneitem_get_source(scene_item)
                width = obs.obs_source_get_width(item_source)
                height = obs.obs_source_get_height(item_source)

                # Make sure it's loaded correctly
                if width > 0 and height > 0:
                    scale_x = 50 / width
                    scale_y = 50 / height
                    scale = obs.vec2()
                    obs.vec2_set(scale, scale_x, scale_y)
                    obs.obs_sceneitem_set_scale(scene_item, scale)

                if "Logo" in source_data["name"]:
                    scale_x = 200 / width
                    scale_y = 200 / height
                    scale = obs.vec2()
                    obs.vec2_set(scale, scale_x, scale_y)
                    obs.obs_sceneitem_set_scale(scene_item, scale)

        # Set position (x, y)
        position = source_data.get("position", {})
        if position:
            scene_item = obs.obs_scene_find_source(scene_source, source_name)
            if scene_item:
                vec = obs.vec2()
                obs.vec2_set(vec, position.get("x", 0.0), position.get("y", 0.0))
                obs.obs_sceneitem_set_pos(scene_item, vec)

        if source_type == "text_gdiplus":
            obs.obs_data_release(font_settings)
            obs.obs_data_release(source_settings)
            obs.obs_source_release(source)
        elif source_type == "image_source":
            obs.obs_data_release(source_settings)
            obs.obs_source_release(source)

    # Release the scene reference
    obs.obs_scene_release(scene_source)
