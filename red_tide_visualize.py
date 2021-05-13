import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from utils import *
import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

# Coords at 31 N, 87 W
northwest_x = 130
northwest_y = 69

# Coords at 25 N, 80 W
southeast_x = 777
southeast_y = 625

textanchor_x = 324
textanchor_y = 7

file_path = 'PinellasMonroeCoKareniabrevis 2010-2020.06.12.xlsx'

df = pd.read_excel(file_path)

lastyear = -1
lastmonth = -1
lastday = -1

xs = []
ys = []
redtide_concs = []
lifetimes = []

initial_lifetime = 5

firstday = True

out_folder = 'output_images'
ensure_folder(out_folder)
daynumber = 0

for i in range(0, df.shape[0]):
	importdate = df.at[i, 'Sample Date']
	latitude = df.at[i, 'Latitude']
	longitude = abs(df.at[i, 'Longitude'])
	redtide_conc = df.at[i, 'Karenia brevis abundance (cells/L)']

	x, y = findLatLongInArray(northwest_x, northwest_y, southeast_x, southeast_y, latitude, longitude)

	year = importdate.year
	month = importdate.month
	day = importdate.day
	print('Processing ' + str(month) + '/' + str(day) + '/' + str(year) + '...')
	if(year == lastyear and month == lastmonth and day == lastday):
		xs.append(x)
		ys.append(y)
		redtide_concs.append(redtide_conc)
		lifetimes.append(initial_lifetime)
	else:
		if(firstday == True):
			firstday = False
		else:
			#Plot the days between the last day and this day
			lastday = date(lastyear, lastmonth, lastday)
			thisday = date(year, month, day)
			timediff = thisday - lastday
			for k in range(timediff.days):
				im = Image.open('florida-map.jpg')

				img1 = ImageDraw.Draw(im, 'RGBA')
				for j in range(len(xs)):
					color = None
					opacity = round((lifetimes[j]/initial_lifetime)*255)
					# Key for red tide concentrations from https://myfwc.com/research/redtide/statewide/
					if(redtide_concs[j] < 1000):
						color = (128, 128, 128, opacity)
						radius = 3
					elif(redtide_concs[j] > 1000 and redtide_concs[j] < 10000):
						color = (255, 255, 255, opacity)
						radius = 6
					elif(redtide_concs[j] > 10000 and redtide_concs[j] < 100000):
						color = (255, 255, 0, opacity)
						radius = 9
					elif(redtide_concs[j] > 100000 and redtide_concs[j] < 1000000):
						color = (255, 165, 0, opacity)
						radius = 12
					elif(redtide_concs[j] > 1000000):
						color = (255, 0, 0, opacity)
						radius = 15
					img1.ellipse([(xs[j]-radius, ys[j]-radius), (xs[j]+radius, ys[j]+radius)], fill=color, outline=color)
					lifetimes[j] = lifetimes[j] - 1

				currentdate = lastday + timedelta(days=k)
				fnt = ImageFont.truetype("arial.ttf", 35)
				img1.text((textanchor_x, textanchor_y), str(currentdate.month) + '/' + str(currentdate.day) + '/' + str(currentdate.year), font=fnt, fill=(0,0,0,255))
				im.save(out_folder+'/image' + str(daynumber).zfill(5) + '.png')
				daynumber = daynumber + 1
				im.close()

				#Remove samples with expired lifetimes
				expired_inds = [inds for inds, lifetimes in enumerate(lifetimes) if lifetimes <= 0]
				while(expired_inds != []):
					del xs[expired_inds[0]]
					del ys[expired_inds[0]]
					del redtide_concs[expired_inds[0]]
					del lifetimes[expired_inds[0]]
					expired_inds = [inds for inds, lifetimes in enumerate(lifetimes) if lifetimes <= 0]

		xs.append(x)
		ys.append(y)
		redtide_concs.append(redtide_conc)
		lifetimes.append(initial_lifetime)
		lastyear = year
		lastmonth = month
		lastday = day