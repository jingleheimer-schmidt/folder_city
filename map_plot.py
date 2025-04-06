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

def draw_map(BASE_PATH, LOCATIONS, STREET_NAMES, AVENUE_NAMES, STREET_NUMBERS, AVENUE_NUMBERS):
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
    # plt.show()
