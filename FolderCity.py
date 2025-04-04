import os
import random
import shutil
from pathlib import Path
from typing import List, Dict, Union

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
BASE_PATH = Path(os.getcwd())
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

LOCATIONS = [
    {
        "name": "the library",
        "block_location": "horizontals/Juniper St blocks/2000-2099 Juniper St",
        "address": "2025 Juniper St - the library",
        "exit_name": "front door",
        "marker": "[ the library ]",
        "objects": [
            {"path": "fiction books/a brief history of map quests"},
            {"path": "fiction books/home, again"},
            {"path": "fiction books/deep ocean"},
            {"path": "fiction books/hello ily"},
            {"path": "fiction books/goblin tomb 2"},
            {"path": "fiction books/lost in the woods"},
            {"path": "fiction books/one more time"},
            {"path": "nonfiction books/the second house"},
            {"path": "nonfiction books/in too deep- a true story of the ultimate unsinkable submarine"},
            {"path": "nonfiction books/how to identify animal bites"},
            {"path": "nonfiction books/nobody knows"},
            {"path": "nonfiction books/snakes"},
            {"path": "nonfiction books/what's that sound?"},
        ]
    },
    {
        "name": "california drive park",
        "block_location": "verticals/California Dr blocks/300-399 California Dr",
        "address": "301 California Dr - california drive park",
        "exit_name": "sidewalk",
        "marker": "[ california drive park ]",
        "objects": [
            {"path": "tree", "min": 1, "max": 15, "chance": 0.1},
            {"path": "shrub", "min": 32, "max": 85, "chance": 0.05},
            {"path": "postcard"},
            {"path": "trashcan/compostable plastic utensils"},
            {"path": "trashcan/paper plates"},
            {"path": "trashcan/garbage"},
            {"path": "park bench dedicated to gideon"},
            {"path": "park bench dedicated to the ghosts"},
            {"path": "public bathroom/toilet"},
            {"path": "public bathroom/sink"},
            {"path": "public bathroom/shattered mirror"},
        ]
    },
    {
        "name": "market deli",
        "block_location": "verticals/Market Ave blocks/600-699 Market Ave",
        "address": "662 Market Ave - market deli",
        "exit_name": "front door",
        "marker": "[ market deli ]",
        "objects": [
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
    },
    {
        "name": "rosenberg botanicals",
        "block_location": "horizontals/Willow St blocks/1900-1999 Willow St",
        "address": "1981 Willow St - rosenberg botanicals",
        "exit_name": "front door",
        "marker": "[ rosenberg botanicals ]",
        "objects": [
            {"path": "bouquets/ornate_bouquet", "min": 1, "max": 5, "chance": 0.75},
            {"path": "bouquets/simple_bouquet", "min": 3, "max": 10, "chance": 0.75},
            {"path": "bouquets/assorted_roses", "min": 3, "max": 6, "chance": 0.75},
            {"path": "bouquets/assorted_tulips", "min": 3, "max": 7, "chance": 0.75},
            {"path": "potted plants/small_succulent", "min": 5, "max": 15, "chance": 0.5},
            {"path": "potted plants/snakeplant", "min": 5, "max": 15, "chance": 0.4},
            {"path": "potted plants/small_fern", "min": 2, "max": 10, "chance": 0.6},
            {"path": "seed packs/carrot_seeds", "min": 1, "max": 15, "chance": 0.4},
            {"path": "seed packs/parsley_seeds", "min": 1, "max": 15, "chance": 0.4},
            {"path": "seed packs/thyme_seeds", "min": 1, "max": 15, "chance": 0.4},
            {"path": "seed packs/tomato_seeds", "min": 1, "max": 15, "chance": 0.4},
            {"path": "seed packs/beet_seeds", "min": 1, "max": 15, "chance": 0.4},
            {"path": "seed packs/onion_seeds", "min": 1, "max": 15, "chance": 0.4},
            {"path": "seed packs/cucumber_seeds", "min": 1, "max": 15, "chance": 0.4},
            {"path": "storeroom/seed of wonder"},
            {"path": "cash register"},
        ],
    },
    {
        "name": "the observatory",
        "block_location": "horizontals/Oak St blocks/2200-2299 Oak St",
        "address": "2222 Oak St - the observatory",
        "exit_name": "front gate",
        "marker": "[ the observatory ]",
        "objects": [
            {"path": "telescope"},
            {"path": "research papers/black hole theories"},
            {"path": "research papers/astronomical charts"},
            {"path": "control room/switchboard"},
            {"path": "control room/old radio transmitter"},
            {"path": "storage room/spare telescope lens"},
            {"path": "notepad with cryptic star coordinates"},
            {"path": "gift shop/souvenir_moon_rock", "min": 1, "max": 5, "chance": 0.5},
            {"path": "gift shop/comet_postcard", "min": 1, "max": 10, "chance": 0.6},
            {"path": "gift shop/moon_phase_postcard", "min": 1, "max": 10, "chance": 0.6},
            {"path": "gift shop/star_earrings", "min": 1, "max": 5, "chance": 0.5},
        ],
    },
    {
        "name": "rooftop café",
        "block_location": "verticals/Sunset Ln blocks/300-399 Sunset Ln",
        "address": "350 Sunset Ln - rooftop café",
        "exit_name": "exit stairwell",
        "marker": "[ rooftop café ]",
        "objects": [
            {"path": "barista counter/espresso machine"},
            {"path": "table/croissant"},
            {"path": "table/cup of coffee (half empty)"},
            {"path": "shelf/poetry book"},
            {"path": "lost and found/scarf"},
            {"path": "patio/telescope"},
            {"path": "patio/table for two"},
            {"path": "balcony/viewfinder (out of order)"},
            {"path": "balcony/viewfinder"},
        ],
    },
    {
        "name": "underground bunker",
        "block_location": "horizontals/Chestnut St blocks/2100-2199 Chestnut St",
        "address": "2150 Chestnut St - underground bunker",
        "exit_name": "steel door",
        "marker": "[ underground bunker ]",
        "objects": [
            {"path": "control room/flickering light"},
            {"path": "radio equipment/static hum"},
            {"path": "food storage/canned_beans", "min": 10, "max": 30, "chance": 0.7},
            {"path": "sleeping quarters/bunk bed"},
            {"path": "abandoned diary"},
            {"path": "generator (low power)"},
            {"path": "emergency exit (sealed shut)"},
        ],
    },
]

# Run setup functions
reset_map_contents()
setup_streets_and_avenues()
setup_navigation()
setup_welcome_center()

for location in LOCATIONS:
    sidewalk = MAP_CONTENTS / location["block_location"]
    building = MAP_CONTENTS / location["block_location"] / location["address"]
    create_file(building / location["marker"])
    create_symlink(sidewalk, building / location["exit_name"])
    create_objects(building, location["objects"])



import matplotlib.pyplot as plt
from adjustText import adjust_text

# --- Helper Functions ---
def parse_address(address):
    """
    Returns (number, road) from an address string.
    e.g. "2222 Oak St - the observatory" -> (2222, "Oak St")
    """
    main_part = address.split(" - ")[0]
    parts = main_part.split()
    try:
        num = int(parts[0])
    except ValueError:
        return None, None
    road = " ".join(parts[1:])
    return num, road

def get_block_index(num, block_ranges):
    """
    For a numeric address and a list of block ranges like "2000-2099",
    returns (index, low, high) if found, else (None, None, None).
    """
    for i, rng in enumerate(block_ranges):
        low_str, high_str = rng.split('-')
        low = int(low_str)
        high = int(high_str)
        if low <= num <= high:
            return i, low, high
    return None, None, None

# --- Create the Plot ---
# Use a light background for a softer look.
fig, ax = plt.subplots(figsize=(8, 8))

# Draw grid lines only for the named streets (y=0..6) and avenues (x=0..6).
# Use a dotted, semi-transparent line style.
for i in range(len(STREET_NAMES)):  # y = 0 .. 6
    ax.axhline(y=i, color='gray', linestyle=':', linewidth=0.8, alpha=0.7)
for i in range(len(AVENUE_NAMES)):   # x = 0 .. 6
    ax.axvline(x=i, color='gray', linestyle=':', linewidth=0.8, alpha=0.7)

# Add the welcome center to the locations list
LOCATIONS.append({
    "name": "the welcome center",
    "block_location": "horizontals/Juniper St blocks/1900-1999 Juniper St",
    "address": "1995 Juniper St - the welcome center"
})

texts = []  # We'll collect the text objects here
x_points = []
y_points = []

# Plot each location.
for loc in LOCATIONS:
    num, road = parse_address(loc["address"])
    if num is None or road is None:
        continue
    label = f"{loc['name']}\n{num} {road}"

    # For horizontal (street) addresses:
    if road in STREET_NAMES:
        street_idx = STREET_NAMES.index(road)
        block_idx, low, high = get_block_index(num, STREET_NUMBERS)
        if block_idx is None:
            continue
        # Adjust the block index so that a block like "2000-2099" (index 4) appears between avenue 3 and 4.
        adjusted_block_idx = block_idx - 1 if block_idx > 0 else block_idx
        rel_x = (num - low) / (high - low)
        x = adjusted_block_idx + rel_x
        y = street_idx  # exactly on the street line
        ax.plot(x, y, 'o', color='tab:blue', markersize=8)
        # Slight offset for readability:
        # Use `annotate` instead of `text`
        txt = ax.annotate(
            label,
            xy=(x, y),                 # the point (data coords)
            xytext=(x, y - 0.5),       # label placed above (because of invert_yaxis)
            textcoords='data',         # interpret xytext in data coords
            ha='center', va='bottom',
            arrowprops=dict(
                arrowstyle='->',
                color='gray',
                alpha=0.5
            ),
            bbox=dict(
                boxstyle='round,pad=0.2',
                fc='white',            # facecolor
                ec='none',             # edgecolor
                alpha=0.7
            ),
            fontsize=8,
            color='black'
        )
        texts.append(txt)
    
    # For vertical (avenue) addresses:
    elif road in AVENUE_NAMES:
        avenue_idx = AVENUE_NAMES.index(road)
        block_idx, low, high = get_block_index(num, AVENUE_NUMBERS)
        if block_idx is None:
            continue
        adjusted_block_idx = block_idx - 1 if block_idx > 0 else block_idx
        rel_y = (num - low) / (high - low)
        x = avenue_idx  # exactly on the avenue line
        y = adjusted_block_idx + rel_y
        ax.plot(x, y, '^', color='tab:orange', markersize=8)
        # Use `annotate` instead of `text`
        txt = ax.annotate(
            label,
            xy=(x, y),                 # the point (data coords)
            xytext=(x, y - 0.5),       # label placed above (because of invert_yaxis)
            textcoords='data',         # interpret xytext in data coords
            ha='center', va='bottom',
            arrowprops=dict(
                arrowstyle='->',
                color='gray',
                alpha=0.5
            ),
            bbox=dict(
                boxstyle='round,pad=0.2',
                fc='white',            # facecolor
                ec='none',             # edgecolor
                alpha=0.7
            ),
            fontsize=8,
            color='black'
        )
        texts.append(txt)

# Use adjustText to automatically reposition overlapping labels.
adjust_text(
    texts,
    ax=ax,
    # arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5),
    force_points=1,               # Increase this if labels still collide with markers
    expand_points=(3, 3),       # Enlarge the “no-go” area around each marker
    avoid_self= True,
)

# Remove the outer bounding box (all spines).
for spine in ax.spines.values():
    spine.set_visible(False)

# Set neat axes limits with a bit of padding.
ax.set_xlim(-0.2, len(AVENUE_NAMES) - 1 + 0.2)
ax.set_ylim(-0.2, len(STREET_NAMES) - 1 + 0.2)

# Label axes with the avenue names (x-axis) and street names (y-axis).
ax.set_xticks(range(len(AVENUE_NAMES)))
ax.set_xticklabels(AVENUE_NAMES, rotation=45, ha='right')
ax.set_yticks(range(len(STREET_NAMES)))
ax.set_yticklabels(STREET_NAMES)

# Optionally invert the y-axis so the first street is at the top.
ax.invert_yaxis()

ax.set_title("Folder City Map", fontsize=12)
plt.tight_layout()

# Define the output path in the welcome center folder.
welcome_center = BASE_PATH / "the welcome center"
output_path = welcome_center / "frammed_map.png"

# Save the figure as a PNG file with a high DPI (for good quality).
plt.savefig(str(output_path), dpi=300)

# Optionally, then show the figure.
plt.show()
