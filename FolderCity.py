import os
import random
from pathlib import Path

# Define street and avenue names
STREET_NAMES = [
    "Birch St", "Chestnut St", "Oak St", "Juniper St",
    "Pine St", "Maple St", "Willow St"
]

AVENUE_NAMES = [
    "Ocean Ave", "California Dr", "Mission Ave", "Hollow Dr",
    "Sunset Ln", "Broad Way", "Market Ave"
]

STREET_NUMBERS = [
    "1600-1699", "1700-1799", "1800-1899", "1900-1999",
    "2000-2099", "2100-2199", "2200-2299"
]

AVENUE_NUMBERS = [
    "100-199", "200-299", "300-399", "400-499",
    "500-599", "600-699", "700-799"
]

# Define key locations
BASE_PATH = Path(os.getcwd())
MAP_CONTENTS = BASE_PATH / "the welcome center/basement/unmarked box/flash drive/users/home/library/application support/folder city/map contents"

def create_directory(path):
    """Create a directory if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)

def create_empty_file(path):
    """Create an empty file, ensuring the parent directory exists first."""
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directory exists
    if not path.exists():
        path.write_text("")

def create_symlink(target, link_name):
    """Create a symbolic link if it doesn't already exist."""
    if not link_name.exists():
        os.symlink(target, link_name)

def setup_streets_and_avenues():
    """Create directories for streets, avenues, and their intersections."""
    for street in STREET_NAMES:
        street_path = MAP_CONTENTS / f"horizontals/{street} blocks"
        create_directory(street_path)
        
        for st_number in STREET_NUMBERS:
            block_path = street_path / f"{st_number} {street}"
            create_directory(block_path)
            create_empty_file(block_path / f"[ {st_number} {street} ]")

            for avenue in AVENUE_NAMES:
                avenue_path = MAP_CONTENTS / f"verticals/{avenue} blocks"
                create_directory(avenue_path)
                
                for av_number in AVENUE_NUMBERS:
                    av_block_path = avenue_path / f"{av_number} {avenue}"
                    create_directory(av_block_path)
                    create_empty_file(av_block_path / f"[ {av_number} {avenue} ]")
                    
                    intersection_path = MAP_CONTENTS / f"intersections/{street} & {avenue}"
                    create_directory(intersection_path)
                    create_empty_file(intersection_path / f"[ {street} & {avenue} ]")

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

def create_objects(base_path, objects):
    for obj in objects:
        min = obj.get("min", 1)
        max = obj.get("max", obj.get("count", 1))
        chance = obj.get("chance", 1.0)
        for i in range(min, max + 1):
            if random.random() < chance:
                suffix = f"_{i:03}" if max > 1 else ""  # format as three-digit number if more than 1 item
                create_empty_file(base_path / f"{obj['path']}{suffix}")

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
    create_empty_file(welcome_center / "[ the welcome center ]")

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
        create_empty_file(paperclip_box / f"paperclip {i}")

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
        create_empty_file(BASE_PATH / f"the welcome center/{item}")

    create_empty_file(BASE_PATH / "the welcome center/kitchen/stove/large pot/ladle")
    create_empty_file(BASE_PATH / "the welcome center/kitchen/stove/large pot/potato stew?")

    # Kitchen utensils
    clean_chance = 1
    for i in range(12, 21):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/cabinet/drawer/utensil tray/forks/fork_00{prefix}{i}")
        else:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/fork_00{prefix}{i}")
    for i in range(15, 26):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/cabinet/drawer/utensil tray/spoons/spoon_00{prefix}{i}")
        else:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/spoon_00{prefix}{i}")
    for i in range(7, 14):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/cabinet/drawer/utensil tray/knives/knife_00{prefix}{i}")
        else:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/knife_00{prefix}{i}")
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
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/cabinet/top shelf/cup_00{prefix}{i}")
        else:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/cup_00{prefix}{i}")
    for i in range(1, 13):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/cabinet/middle shelf/large_plate_00{prefix}{i}")
        else:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/large_plate_00{prefix}{i}")
        if random.random() < clean_chance:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/cabinet/middle shelf/small_plate_00{prefix}{i}")
        else:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/small_plate_00{prefix}{i}")
    for i in range(1, 9):
        prefix = "0" if i < 10 else ""
        if random.random() < clean_chance:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/cabinet/bottom shelf/bowl_00{prefix}{i}")
        else:
            create_empty_file(BASE_PATH / f"the welcome center/kitchen/dishwasher/bowl_00{prefix}{i}")

def setup_library():
    """Create the library building."""
    block_location = MAP_CONTENTS / "horizontals/Juniper St blocks/2000-2099 Juniper St"
    library_path = block_location / "2025 Juniper St - the library"
    create_empty_file(library_path / "[ the juniper st library ]")
    create_symlink(block_location, library_path / "front door")
    fiction_books = [ "a brief history of map quests", "home, again", "deep ocean", "hello ily", "goblin tombs 2" ]
    nonfiction_books = [ "the second house", "in too deep: the true story of the ultimate unsinkable submarine", "how to identify animal bites", "nobosy knows"]
    for book in fiction_books:
        create_empty_file(library_path / f"fiction/{book}")
    for book in nonfiction_books:
        create_empty_file(library_path / f"nonfiction/{book}")

def setup_california_dr_park():
    """Create the California Dr park."""
    block_location = MAP_CONTENTS / "verticals/California Dr blocks/300-399 California Dr"
    park_path = block_location / "301 California Dr - california drive park"
    create_empty_file(park_path / "[ california drive park ]")
    create_symlink(block_location, park_path / "sidewalk")
    objects = [
        {"path": "tree_07", "count": 1},
        {"path": "tree_04", "count": 1},
        {"path": "tree_11", "count": 1},
        {"path": "shrub_22", "count": 1},
        {"path": "shrub_31", "count": 1},
        {"path": "tree_01", "count": 1},
        {"path": "postcard", "count": 1},
        {"path": "trashcan/compostable plastic utensils", "count": 1},
        {"path": "trashcan/dirty paper plates", "count": 1},
        {"path": "trashcan/garbage", "count": 1},
        {"path": "park bench dedicated to gideon", "count": 1},
        {"path": "park bench dedicated to the ghosts", "count": 1},
    ]
    create_objects(park_path, objects)
    locations = ["public bathroom", "trashcan"]
    for location in locations:
        create_directory(park_path / location)

def setup_market_ave_deli():
    """Create the market ave deli"""
    block_location = MAP_CONTENTS / "verticals/Market Ave blocks/600-699 Market Ave"
    deli_path = block_location / "662 Market Ave - market deli"
    create_empty_file(deli_path / "[ market deli ]")
    create_symlink(block_location, deli_path / "front door")
    objects = [
        {"path": "refrigerator/lemonade", "min": 15, "max": 30, "chance": 0.125},
        {"path": "refrigerator/iced_coffee", "min": 10, "max": 25, "chance": 0.25},
        {"path": "freezer/popsicle", "min": 10, "max": 25, "chance": 0.25},
        {"path": "garbage can/popsicle_stick", "min": 1, "max": 100, "chance": 0.03},
        {"path": "garbage can/empty_cup", "min": 1, "max": 100, "chance": 0.03},
        {"path": "sandwhich counter/sandwhich", "min": 25, "max": 55, "chance": 0.25},
        {"path": "chair", "min": 1, "max": 8, "chance": 1.0},
        {"path": "cash register", "count": 1},
        {"path": "muted tv", "count": 1},
        {"path": "table", "count": 2},
    ]
    create_objects(deli_path, objects)

# Run setup functions
setup_streets_and_avenues()
setup_navigation()
setup_welcome_center()
setup_library()
setup_california_dr_park()
setup_market_ave_deli()
