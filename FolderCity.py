import os
from pathlib import Path

# here are my tables of values
street_names = [
    "Birch St",
    "Chestnut St",
    "Oak St",
    "Juniper St",
    "Pine St",
    "Maple St",
    "Willow St"
]
avenue_names = [
    "Ocean Ave",
    "California Dr",
    "Mission Ave",
    "Hollow Dr",
    "Sunset Ln",
    "Broad Way",
    "Market Ave"
]
street_numbers = [
    "1600-1699",
    "1700-1799",
    "1800-1899",
    "1900-1999",
    "2000-2099",
    "2100-2199",
    "2200-2299",
    # "2300-2399"
]
avenue_numbers = [
    "100-199",
    "200-299",
    "300-399",
    "400-499",
    "500-599",
    "600-699",
    "700-799",
    # "100-199",
]

og_path = os.getcwd()  # this one gets the current path of where the py file is located
basement = Path(f"{og_path}/the welcome center/go to the basement")
application_support = Path(f"{basement}/unmarked box/old usb flash drive/users/home/library/application support")
path = f"{application_support}/folder city alpha/map contents"

for street in street_names:
    street_path = Path(f"{path}/horizontals/{street} blocks")
    os.makedirs(street_path, exist_ok=True)  # make the street block folders
    for st_number in street_numbers:
        os.makedirs(f"{street_path}/{st_number} {street}", exist_ok=True)  # make the block number folders
        Path(f"{street_path}/{st_number} {street}/{st_number} {street}").write_text("")  # write the signpost files
        for avenue in avenue_names:
            avenue_path = Path(f"{path}/verticals/{avenue} blocks")
            os.makedirs(avenue_path, exist_ok=True)
            for av_number in avenue_numbers:
                os.makedirs(f"{avenue_path}/{av_number} {avenue}", exist_ok=True)  # make the block number folders
                Path(f"{avenue_path}/{av_number} {avenue}/{av_number} {avenue}").write_text("")  # create the signposts

                intersection_path = Path(f"{path}/intersections/{street} & {avenue}")
                os.makedirs(intersection_path, exist_ok=True)
                Path(f"{intersection_path}/{street} & {avenue}").write_text("")

for street in street_names:
    street_path = Path(f"{path}/horizontals/{street} blocks")
    # index = street_names.index(street)
    for st_number in street_numbers:
        index = street_numbers.index(st_number)
        block = Path(f"{street_path}/{st_number} {street}")
        east_avenue = avenue_names[index]
        west_avenue = avenue_names[index - 1]
        east_intersection = Path(f"{path}/intersections/{street} & {east_avenue}")
        west_intersection = Path(f"{path}/intersections/{street} & {west_avenue}")
        if index == 0:
            os.symlink(block, Path(f"{east_intersection}/go west to {st_number} {street}"))
            os.symlink(east_intersection, Path(f"{block}/go east to {street} & {east_avenue}"))

        # elif index == street_numbers.index(street_numbers[-1]):
        #     os.symlink(block, Path(f"{west_intersection}/go east to {st_number} {street}"))
        #     os.symlink(west_intersection, Path(f"{block}/go west to {street} & {west_avenue}"))
        #
        #     os.symlink(block, Path(f"{east_intersection}/go west to {st_number} {street}"))
        #     os.symlink(east_intersection, Path(f"{block}/go east to {street} & {east_avenue}"))

        else:
            os.symlink(block, Path(f"{east_intersection}/go west to {st_number} {street}"))
            os.symlink(east_intersection, Path(f"{block}/go east to {street} & {east_avenue}"))

            os.symlink(block, Path(f"{west_intersection}/go east to {st_number} {street}"))
            os.symlink(west_intersection, Path(f"{block}/go west to {street} & {west_avenue}"))

for avenue in avenue_names:
    avenue_path = Path(f"{path}/verticals/{avenue} blocks")
    # index = street_names.index(street)
    for av_number in avenue_numbers:
        index = avenue_numbers.index(av_number)
        south_street = street_names[index]
        north_street = street_names[index - 1]
        block = Path(f"{avenue_path}/{av_number} {avenue}")
        south_intersection = Path(f"{path}/intersections/{south_street} & {avenue}")
        north_intersection = Path(f"{path}/intersections/{north_street} & {avenue}")
        if index == 0:
            os.symlink(block, Path(f"{south_intersection}/go north to {av_number} {avenue}"))
            os.symlink(south_intersection, Path(f"{block}/go south to {south_street} & {avenue}"))

        # elif index == avenue_numbers.index(avenue_numbers[-1]):
        #     os.symlink(block, Path(f"{north_intersection}/go south to {av_number} {avenue}"))
        #     os.symlink(north_intersection, Path(f"{block}/go north to {north_street} & {avenue}"))
        #
        #     os.symlink(block, Path(f"{south_intersection}/go north to {av_number} {avenue}"))
        #     os.symlink(south_intersection, Path(f"{block}/go south to {south_street} & {avenue}"))

        else:
            os.symlink(block, Path(f"{south_intersection}/go north to {av_number} {avenue}"))
            os.symlink(south_intersection, Path(f"{block}/go south to {south_street} & {avenue}"))

            os.symlink(block, Path(f"{north_intersection}/go south to {av_number} {avenue}"))
            os.symlink(north_intersection, Path(f"{block}/go north to {north_street} & {avenue}"))

os.makedirs(f"{basement}/unmarked box/old usb flash drive/users/guest")
os.makedirs(f"{basement}/unmarked box/old usb flash drive/users/home/movies")
os.makedirs(f"{basement}/unmarked box/old usb flash drive/users/home/music")
os.makedirs(f"{basement}/unmarked box/old usb flash drive/users/home/pictures")
os.makedirs(f"{basement}/unmarked box/old usb flash drive/users/home/public")
os.makedirs(f"{basement}/unmarked box/old usb flash drive/users/home/downloads")
os.makedirs(f"{basement}/unmarked box/old usb flash drive/users/home/applications/folder city")
os.makedirs(f"{basement}/filing cabinet/open top drawer")
os.makedirs(f"{basement}/filing cabinet/open middle drawer")
os.makedirs(f"{basement}/filing cabinet/open bottom drawer")
os.makedirs(f"{basement}/unmarked box/box of paperclips")
i = 1
while i <= 250:
    Path(f"{basement}/unmarked box/box of paperclips/paperclip {i}").write_text("")
    i += 1
os.makedirs(f"{og_path}/the welcome center/go upstairs/go to the balcony")
os.makedirs(f"{og_path}/the welcome center/go upstairs/go to the washroom")
os.makedirs(f"{og_path}/the welcome center/go upstairs/go to the bedroom/open dresser")
Path(f"{og_path}/the welcome center/go upstairs/go to the bedroom/a bed").write_text("")
Path(f"{og_path}/the welcome center/go upstairs/go to the washroom/a toilet").write_text("")
Path(f"{og_path}/the welcome center/go upstairs/go to the washroom/a sink").write_text("")
Path(f"{og_path}/the welcome center/go upstairs/go to the washroom/a bathtub").write_text("")
os.makedirs(f"{og_path}/the welcome center/go to the living room")
os.makedirs(f"{og_path}/the welcome center/go to the kitchen")
Path(f"{og_path}/the welcome center/go to the kitchen/a stove").write_text("")
Path(f"{og_path}/the welcome center/go to the kitchen/a sink").write_text("")
Path(f"{og_path}/the welcome center/go to the kitchen/a table").write_text("")

welcome_center = Path(f"{og_path}/the welcome center")
wc_sym = Path(f"{path}/horizontals/Juniper St blocks/1900-1999 Juniper St/1995 Juniper St - the welcome center")
os.symlink(welcome_center, wc_sym)

block_location = Path(f"{path}/horizontals/Juniper St blocks/1900-1999 Juniper St")
door_location = Path(f"{welcome_center}/go out the front door")
os.symlink(block_location, door_location)

app_folder = Path(f"{basement}/unmarked box/old usb flash drive/users/home/applications/folder city/the welcome center")
os.symlink(welcome_center, app_folder)
Path(f"{og_path}/the welcome center/the welcome center").write_text("")
