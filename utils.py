import os

# Northwest coords at 31 N, 87 W
# Southeast coords at 25 N, 80 W
def findLatLongInArray(northwest_x, northwest_y, southeast_x, southeast_y, latitude, longitude):
	long_percentmove = (87 - longitude)/(87 - 80)

	x = round(northwest_x + long_percentmove*(southeast_x - northwest_x))

	lat_percentmove = (31 - latitude)/(31 - 25)

	y = round(northwest_y + lat_percentmove*(southeast_y - northwest_y))

	return x, y

def ensure_folder(folder):
	if not os.path.isdir(folder):
		os.mkdir(folder)