import os
import sys
import random
import shutil
import platform
import subprocess
import pyfiglet
import time
from tqdm import tqdm
from pathlib import Path
from typing import List, Dict, Union
from locations import LOCATIONS
from map_plot import draw_map

# Define street and avenue names
STREET_NAMES = [
    "Birch St",
    "Chestnut St",
    "Oak St",
    "Juniper St",
    "Pine St",
    "Maple St",
    "Willow St",
]

AVENUE_NAMES = [
    "Ocean Ave",
    "California Dr",
    "Mission Ave",
    "Hollow Dr",
    "Sunset Ln",
    "Broad Way",
    "Market Ave",
]

STREET_NUMBERS = [
    "1600-1699",
    "1700-1799",
    "1800-1899",
    "1900-1999",
    "2000-2099",
    "2100-2199",
    "2200-2299",
]

AVENUE_NUMBERS = [
    "100-199",
    "200-299",
    "300-399",
    "400-499",
    "500-599",
    "600-699",
    "700-799",
]

# Define key locations
if getattr(sys, 'frozen', False):
    # If the application is bundled as an executable, use the directory of the executable.
    BASE_PATH = Path(sys.executable).parent
else:
    # If running in a regular Python environment, use the directory of the script.
    BASE_PATH = Path(__file__).parent
MAP_CONTENTS = BASE_PATH / "the welcome center/basement/unmarked box/flash drive/users/home/library/application support/folder city/map contents"

def reset_map_contents():
    """Delete the welcome center folder if it already exists"""
    welcome_center = BASE_PATH / "the welcome center"
    if welcome_center.exists():
        shutil.rmtree(welcome_center)

def create_directory(path):
    """Create a directory if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)

def create_file(path: Path, contents: str = ""):
    """Create a file with optional contents, ensuring the parent directory exists first."""
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directory exists
    if not path.exists():
        path.write_text(contents)

def create_symlink(target, destination):
    """Create a symbolic link to target if it doesn't already exist. Destination is the symlink path and target is the file to link to."""
    if not destination.exists():
        os.symlink(target, destination)

def setup_streets_and_avenues():
    """Create directories for streets, avenues, and their intersections."""
    for street in STREET_NAMES:
        street_path = MAP_CONTENTS / f"horizontals/{street} blocks"
        create_directory(street_path)
        
        for st_number in STREET_NUMBERS:
            block_path = street_path / f"{st_number} {street}"
            create_directory(block_path)
            create_file(block_path / f"[ {st_number} {street} ]")

            for avenue in AVENUE_NAMES:
                avenue_path = MAP_CONTENTS / f"verticals/{avenue} blocks"
                create_directory(avenue_path)
                
                for av_number in AVENUE_NUMBERS:
                    av_block_path = avenue_path / f"{av_number} {avenue}"
                    create_directory(av_block_path)
                    create_file(av_block_path / f"[ {av_number} {avenue} ]")
                    
                    intersection_path = MAP_CONTENTS / f"intersections/{street} & {avenue}"
                    create_directory(intersection_path)
                    create_file(intersection_path / f"[ {street} & {avenue} ]")

def setup_navigation():
    """Create symbolic links between streets and avenues for navigation."""
    for street in STREET_NAMES:
        street_path = MAP_CONTENTS / f"horizontals/{street} blocks"

        for index, st_number in enumerate(STREET_NUMBERS):
            block = street_path / f"{st_number} {street}"

            if index < len(AVENUE_NAMES):
                east_avenue = AVENUE_NAMES[index]
                east_intersection = MAP_CONTENTS / f"intersections/{street} & {east_avenue}"
                create_symlink(block, east_intersection / f"⏴ west to {st_number} {street}")
                create_symlink(east_intersection, block / f"⏵ east to {street} & {east_avenue}")

            if index > 0:
                west_avenue = AVENUE_NAMES[index - 1]
                west_intersection = MAP_CONTENTS / f"intersections/{street} & {west_avenue}"
                create_symlink(block, west_intersection / f"⏵ east to {st_number} {street}")
                create_symlink(west_intersection, block / f"⏴ west to {street} & {west_avenue}")

    for avenue in AVENUE_NAMES:
        avenue_path = MAP_CONTENTS / f"verticals/{avenue} blocks"

        for index, av_number in enumerate(AVENUE_NUMBERS):
            block = avenue_path / f"{av_number} {avenue}"

            if index < len(STREET_NAMES):
                south_street = STREET_NAMES[index]
                south_intersection = MAP_CONTENTS / f"intersections/{south_street} & {avenue}"
                create_symlink(block, south_intersection / f"⏶ north to {av_number} {avenue}")
                create_symlink(south_intersection, block / f"⏷ south to {south_street} & {avenue}")

            if index > 0:
                north_street = STREET_NAMES[index - 1]
                north_intersection = MAP_CONTENTS / f"intersections/{north_street} & {avenue}"
                create_symlink(block, north_intersection / f"⏷ south to {av_number} {avenue}")
                create_symlink(north_intersection, block / f"⏶ north to {north_street} & {avenue}")

def create_objects(base_path: Path, objects: List[Dict[str, Union[str, int, float]]]) -> None:
    """Create objects in the specified base path.

    Args:
        base_path (Path): The base directory path where files will be created.
        objects (List[Dict[str, Union[str, int, float]]]): 
            A list of dictionaries, each containing:
                - path (str): The path to create the file.
                - min (int, optional): Minimum number for object naming (ex. obj_001) (default: 1).
                - max (int, optional): Maximum number for object naming (ex. obj_005) (default: count or 1).
                - count (int, optional): Fixed number of objects (overrides min/max).
                - chance (float, optional): Probability (0 to 1) that each object is created (default: 1.0).
    """
    for obj in objects:
        min = obj.get("min", 1)
        max = obj.get("max", obj.get("count", 1))
        chance = obj.get("chance", 1.0)
        contents = obj.get("contents", "")
        for i in range(min, max + 1):
            if random.random() < chance:
                suffix = f"_{i:03}" if max > 1 else ""  # format as three-digit number if more than 1 item
                create_file(base_path / f"{obj['path']}{suffix}")

def setup_welcome_center():
    """Link the welcome center to different locations in the folder city."""
    welcome_center = BASE_PATH / "the welcome center"
    block_location = MAP_CONTENTS / "horizontals/Juniper St blocks/1900-1999 Juniper St"
    basement = welcome_center / "basement"
    home_folder = basement / "unmarked box/flash drive/users/home"

    # Create symbolic links
    create_symlink(welcome_center, block_location / "1995 Juniper St - the welcome center")
    create_symlink(block_location, welcome_center / "front door")

    # Create a marker file
    create_file(welcome_center / "[ the welcome center ]")

    # Home structure
    home_dirs = ["movies", "music", "pictures", "public", "downloads", "applications/folder city"]
    for directory in home_dirs:
        create_directory(basement / f"unmarked box/flash drive/users/home/{directory}")

    app_folder_symlink = home_folder / "applications/folder city/the welcome center"
    create_symlink(welcome_center, app_folder_symlink)

    # Filing cabinet
    filing_drawers = ["top drawer", "middle drawer", "bottom drawer"]
    for drawer in filing_drawers:
        create_directory(basement / f"filing cabinet/{drawer}")

    # Paperclip box
    paperclip_box = basement / "unmarked box/box of paperclips"
    create_directory(paperclip_box)
    for i in range(1, 251):
        create_file(paperclip_box / f"paperclip {i}")

    # Upstairs
    upstairs_paths = [
        "upstairs/balcony",
        "upstairs/bedroom/dresser/top drawer",
        "upstairs/bedroom/dresser/middle drawer",
        "upstairs/bedroom/dresser/bottom drawer",
    ]
    for path in upstairs_paths:
        create_directory(BASE_PATH / f"the welcome center/{path}")

    # Individual items
    item_paths = [
        "upstairs/bedroom/bed",
        "upstairs/washroom/toilet",
        "upstairs/washroom/sink",
        "upstairs/washroom/bathtub",
        "kitchen/sink",
        "kitchen/table",
    ]
    for item in item_paths:
        create_file(BASE_PATH / f"the welcome center/{item}")

    create_file(BASE_PATH / "the welcome center/kitchen/stove/large pot/ladle")
    create_file(BASE_PATH / "the welcome center/kitchen/stove/large pot/potato stew?")

    # Kitchen utensils
    clean_chance = 1
    for i in range(12, 21):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_file(BASE_PATH / f"the welcome center/kitchen/cabinet/drawer/utensil tray/forks/fork_00{prefix}{i}")
        else:
            create_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/fork_00{prefix}{i}")
    for i in range(15, 26):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_file(BASE_PATH / f"the welcome center/kitchen/cabinet/drawer/utensil tray/spoons/spoon_00{prefix}{i}")
        else:
            create_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/spoon_00{prefix}{i}")
    for i in range(7, 14):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_file(BASE_PATH / f"the welcome center/kitchen/cabinet/drawer/utensil tray/knives/knife_00{prefix}{i}")
        else:
            create_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/knife_00{prefix}{i}")
    shelf_paths = [
        "kitchen/cabinet/top shelf",
        "kitchen/cabinet/middle shelf",
        "kitchen/cabinet/bottom shelf",
    ]
    for shelf in shelf_paths:
        create_directory(BASE_PATH / f"the welcome center/{shelf}")
    for i in range(15, 32):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_file(BASE_PATH / f"the welcome center/kitchen/cabinet/top shelf/cup_00{prefix}{i}")
        else:
            create_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/cup_00{prefix}{i}")
    for i in range(1, 13):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_file(BASE_PATH / f"the welcome center/kitchen/cabinet/middle shelf/large_plate_00{prefix}{i}")
        else:
            create_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/large_plate_00{prefix}{i}")
        if random.random() < clean_chance:
            create_file(BASE_PATH / f"the welcome center/kitchen/cabinet/middle shelf/small_plate_00{prefix}{i}")
        else:
            create_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/small_plate_00{prefix}{i}")
    for i in range(1, 9):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_file(BASE_PATH / f"the welcome center/kitchen/cabinet/bottom shelf/bowl_00{prefix}{i}")
        else:
            create_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/bowl_00{prefix}{i}")

def create_locations():
    for location in LOCATIONS:
        sidewalk = MAP_CONTENTS / location["block_location"]
        building = MAP_CONTENTS / location["block_location"] / location["address"]
        create_file(building / location["marker"])
        create_symlink(sidewalk, building / location["exit_name"])
        create_objects(building, location["objects"])

def open_welcome_center():
    welcome_center_path = BASE_PATH / 'the welcome center'
    if platform.system() == 'Windows':
        os.startfile(str(welcome_center_path))
    elif platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['open', str(welcome_center_path)])
    else:  # Linux and others
        subprocess.Popen(['xdg-open', str(welcome_center_path)])


# only run when executed, not while importing
if __name__ == "__main__":

    banner = pyfiglet.figlet_format(text="Folder City", font="cricket")
    print(banner, flush=True)

    def show_progress_bar(description, length):
        with tqdm(total=length, desc=description, bar_format="{l_bar}{bar:50}", ascii=True) as pbar:
            for i in range(length):
                time.sleep(0.02)
                pbar.update(1)

    # Run setup functions
    show_progress_bar("Initializing", random.randint(25, 75))
    # reset_map_contents()

    show_progress_bar("Paving the roads", random.randint(25, 75))
    setup_streets_and_avenues()

    show_progress_bar("Setting up navigation", random.randint(25, 75))
    setup_navigation()

    show_progress_bar("Designing up the Welcome Center", random.randint(25, 75))
    setup_welcome_center()

    show_progress_bar("Constructing buildings", random.randint(25, 75))
    create_locations()

    show_progress_bar("Drawing the map", random.randint(25, 75))
    draw_map(BASE_PATH, LOCATIONS, STREET_NAMES, AVENUE_NAMES, STREET_NUMBERS, AVENUE_NUMBERS)

    # Open the welcome center folder
    # open_welcome_center()

    print("\a", flush=True)  # This sends the ASCII bell character, which may beep in some terminals

    # Exit the program.
    # Note: If this executable was built with the --windowed flag (on Windows or macOS),
    # no terminal window will appear at all. For command-line launched executables, the terminal
    # might stay open unless it was opened solely to run the app.
    sys.exit()
