# Fearless OBS Updater

---

This script updates your sources inside OBS to display the already picked champions of the series.
Currently, it is only possible to track matches of the Prime League.

## Install Python

---

To use the script, you need to download Python 3.9.10 or later from the official Python website.

[Download Python 3.9.10](https://www.python.org/downloads/release/python-3910/)

## Install Requirements

---

### Windows:

Open CMD and run:

`pip install -r /path/to/requirements.txt`

## Setup Script in OBS

---

1. Go to **Tools** -> **Scripts** in OBS.
2. Under **Python-Settings**, insert the location of your local Python directory `C:/Users/{name}/AppData/Local/Programs/Python/Python39`
3. Add the scripts `manual_fearless.py` and `auto_fearless.py` by clicking the **+** icon.
4. Close and reopen OBS to fully initialize the changes.
5. Return to the scripts tab and start using them.

## Setup Sources in OBS

---

The most important part is the naming of the sources!

### Headers (Text Sources):

```
blue_header_1
blue_header_2
blue_header_3
blue_header_4
blue_header_5

red_header_1
red_header_2
red_header_3
red_header_4
red_header_5
```

### Champion Icons (Image Sources):

```
game_1_blue_pick_1_image
game_1_blue_pick_2_image
game_1_blue_pick_3_image
game_1_blue_pick_4_image
game_1_blue_pick_5_image

game_1_red_pick_1_image
game_1_red_pick_2_image
game_1_red_pick_3_image
game_1_red_pick_4_image
game_1_red_pick_5_image

game_2_blue_pick_1_image
[...]
```

Repeat this for all 5 picks and for all 5 games. If you leave one out, you will get error logs, but nothing critical will happen.

## How to Use the Scripts

---

### Auto Fearless

The auto fearless script works automatically. When you open the script, you'll see an input field where you can insert a match URL.

For example:

`https://www.primeleague.gg/de/matches/591905-teamorangegaming-academy-vs-a-one-man-army`

![img.png](examples/auto.png)

After inserting the URL, the overlay will automatically update itself with data from the website.

If you want to update the same match again, press the **reload** button at the bottom of the script window.

![img.png](examples/scripts.png)

By pressing the **Reset Overlay** button, you can clear all sources at once. You can now enter a new URL. If you want to reuse the same URL, you must press **Reset** (**"Zurücksetzen"**) at the bottom of the script window, which clears all input fields.

### Manual Fearless

The manual fearless script is an alternative if the Prime League match on the website is not updated properly.

You can manually enter data in real-time. The input is **not case-sensitive**, champion names can have **whitespaces**, and you can use special characters such as `'` (e.g., "Kha'Zix").

Example:

![img.png](examples/manual.png)

Unlike the auto script, you don't need a special reset button. The script updates dynamically whenever you update the input. To reset everything, just press **Reset** (**"Zurücksetzen"**) at the bottom of the window.

### General Information

- The script will only display an icon if the name is spelled correctly. If there's a typo, no champion icon will be displayed.
- Both scripts share the same sources, meaning changes in one script will overwrite the other.
- If you use the auto script and then open the manual script to change the **first pick on the blue side**, it will overwrite only that specific pick.
- Using the auto script will update the entire overlay and erase any manually entered data that is not part of the match URL.

## FAQ - Coming Soon

---

A FAQ section will be added once common issues arise.

## How to Contribute

---

If you have suggestions to improve the code or want to contribute, feel free to create a pull request.

## Contact Me

---

If you need help or want to be part of the project, contact me via GitHub or email: **lukas.zimmermann147@outlook.com**

## License

---

[MIT License](https://choosealicense.com/licenses/mit/)

**MIT License**

Copyright (c) [2025] [Bauws]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

