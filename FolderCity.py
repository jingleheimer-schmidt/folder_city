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

# Get the current working directory
OG_PATH = Path(os.getcwd())

# Define key locations
BASEMENT = OG_PATH / "the welcome center/go to the basement"
APPLICATION_SUPPORT = BASEMENT / "unmarked box/old usb flash drive/users/home/library/application support"
CITY_PATH = APPLICATION_SUPPORT / "folder city alpha/map contents"

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
        street_path = CITY_PATH / f"horizontals/{street} blocks"
        create_directory(street_path)
        
        for st_number in STREET_NUMBERS:
            block_path = street_path / f"{st_number} {street}"
            create_directory(block_path)
            create_empty_file(block_path / f"[ {st_number} {street} ]")

            for avenue in AVENUE_NAMES:
                avenue_path = CITY_PATH / f"verticals/{avenue} blocks"
                create_directory(avenue_path)
                
                for av_number in AVENUE_NUMBERS:
                    av_block_path = avenue_path / f"{av_number} {avenue}"
                    create_directory(av_block_path)
                    create_empty_file(av_block_path / f"[ {av_number} {avenue} ]")
                    
                    intersection_path = CITY_PATH / f"intersections/{street} & {avenue}"
                    create_directory(intersection_path)
                    create_empty_file(intersection_path / f"[ {street} & {avenue} ]")

def setup_navigation():
    """Create symbolic links between streets and avenues for navigation."""
    for street in STREET_NAMES:
        street_path = CITY_PATH / f"horizontals/{street} blocks"

        for index, st_number in enumerate(STREET_NUMBERS):
            block = street_path / f"{st_number} {street}"

            if index < len(AVENUE_NAMES):
                east_avenue = AVENUE_NAMES[index]
                east_intersection = CITY_PATH / f"intersections/{street} & {east_avenue}"
                create_symlink(block, east_intersection / f"go west to {st_number} {street}")
                create_symlink(east_intersection, block / f"go east to {street} & {east_avenue}")

            if index > 0:
                west_avenue = AVENUE_NAMES[index - 1]
                west_intersection = CITY_PATH / f"intersections/{street} & {west_avenue}"
                create_symlink(block, west_intersection / f"go east to {st_number} {street}")
                create_symlink(west_intersection, block / f"go west to {street} & {west_avenue}")

    for avenue in AVENUE_NAMES:
        avenue_path = CITY_PATH / f"verticals/{avenue} blocks"

        for index, av_number in enumerate(AVENUE_NUMBERS):
            block = avenue_path / f"{av_number} {avenue}"

            if index < len(STREET_NAMES):
                south_street = STREET_NAMES[index]
                south_intersection = CITY_PATH / f"intersections/{south_street} & {avenue}"
                create_symlink(block, south_intersection / f"go north to {av_number} {avenue}")
                create_symlink(south_intersection, block / f"go south to {south_street} & {avenue}")

            if index > 0:
                north_street = STREET_NAMES[index - 1]
                north_intersection = CITY_PATH / f"intersections/{north_street} & {avenue}"
                create_symlink(block, north_intersection / f"go south to {av_number} {avenue}")
                create_symlink(north_intersection, block / f"go north to {north_street} & {avenue}")

def setup_additional_locations():
    """Create additional structures like the welcome center, filing cabinets, and a home directory."""
    # Home structure
    home_dirs = ["movies", "music", "pictures", "public", "downloads", "applications/folder city"]
    for directory in home_dirs:
        create_directory(BASEMENT / f"unmarked box/old usb flash drive/users/home/{directory}")

    # Filing cabinet
    filing_drawers = ["top drawer", "middle drawer", "bottom drawer"]
    for drawer in filing_drawers:
        create_directory(BASEMENT / f"filing cabinet/{drawer}")

    # Paperclip box
    paperclip_box = BASEMENT / "unmarked box/box of paperclips"
    create_directory(paperclip_box)
    for i in range(1, 251):
        create_empty_file(paperclip_box / f"paperclip {i}")

    # Upstairs
    upstairs_paths = [
        "go upstairs/go to the balcony",
        "go upstairs/go to the washroom",
        "go upstairs/go to the bedroom/dresser",
        "go upstairs/go to the bedroom/dresser/top drawer",
        "go upstairs/go to the bedroom/dresser/middle drawer",
        "go upstairs/go to the bedroom/dresser/bottom drawer",
    ]
    for path in upstairs_paths:
        create_directory(OG_PATH / f"the welcome center/{path}")

    # Individual items
    item_paths = [
        "go upstairs/go to the bedroom/bed",
        "go upstairs/go to the washroom/toilet",
        "go upstairs/go to the washroom/sink",
        "go upstairs/go to the washroom/bathtub",
        "go to the kitchen/stove",
        "go to the kitchen/sink",
        "go to the kitchen/table",
    ]
    for item in item_paths:
        create_empty_file(OG_PATH / f"the welcome center/{item}")
    
    # Kitchen utensils
    for i in range(12, 21):
        if random.random() < 0.8:
            create_empty_file(OG_PATH / f"the welcome center/go to the kitchen/cabinet/drawer/utensil tray/forks/fork_00{i}")
    for i in range(15, 26):
        if random.random() < 0.8:
            create_empty_file(OG_PATH / f"the welcome center/go to the kitchen/cabinet/drawer/utensil tray/spoons/spoon_00{i}")
    for i in range(11, 14):
        if random.random() < 0.8:
            create_empty_file(OG_PATH / f"the welcome center/go to the kitchen/cabinet/drawer/utensil tray/knives/knife_00{i}")
    shelf_paths = [
        "go to the kitchen/cabinet/top shelf",
        "go to the kitchen/cabinet/middle shelf",
        "go to the kitchen/cabinet/bottom shelf",
    ]
    for shelf in shelf_paths:
        create_directory(OG_PATH / f"the welcome center/{shelf}")
    for i in range(15, 32):
        if random.random() < 0.8:
            create_empty_file(OG_PATH / f"the welcome center/go to the kitchen/cabinet/top shelf/cup_00{i}")
    for i in range(1, 13):
        if random.random() < 0.8:
            create_empty_file(OG_PATH / f"the welcome center/go to the kitchen/cabinet/middle shelf/large_plate_00{i}")
        if random.random() < 0.8:
            create_empty_file(OG_PATH / f"the welcome center/go to the kitchen/cabinet/middle shelf/small_plate_00{i}")
    for i in range(1, 9):
        if random.random() < 0.8:
            create_empty_file(OG_PATH / f"the welcome center/go to the kitchen/cabinet/bottom shelf/bowl_00{i}")

def setup_welcome_center():
    """Link the welcome center to different locations in the folder city."""
    welcome_center = OG_PATH / "the welcome center"
    block_location = CITY_PATH / "horizontals/Juniper St blocks/1900-1999 Juniper St"

    # Create symbolic links
    create_symlink(welcome_center, block_location / "1995 Juniper St - the welcome center")
    create_symlink(block_location, welcome_center / "go out the front door")
    
    app_folder = BASEMENT / "unmarked box/old usb flash drive/users/home/applications/folder city/the welcome center"
    create_symlink(welcome_center, app_folder)

    # Create a marker file
    create_empty_file(welcome_center / "[ the welcome center ]")

def setup_library():
    """Create the library building."""
    block_location = CITY_PATH / "horizontals/Juniper St blocks/2000-2099 Juniper St"
    library_path = block_location / "2025 Juniper St - the library"
    create_empty_file(library_path / "[ the juniper st library ]")
    create_symlink(block_location, library_path / "go out the front door")

# Run setup functions
setup_streets_and_avenues()
setup_navigation()
setup_additional_locations()
setup_welcome_center()
setup_library()
