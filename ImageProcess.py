#### ImageProcess.py
# Takes a jpg image in white background and prints a version of the image 
# with white pixels as space and non-white pixels as characters.
#
# Authors: Chris Horan, Zeal Yim
# Created: Feb 23 2016
# Last modified: Feb 24 2016 by Zeal
####

from __future__ import print_function
from PIL import Image

THRESHOLD_MARGIN = 0.95 #Filters out near-white pixels
WHITE = 765 #RGB
MAX_HEIGHT_OUTPUT = 300
MAX_WIDTH_OUTPUT = 300

def imgToArr(img): #turn an image into a 2D array. If the image's size is larger than MAX_HEIGHT_OUTPUT or MAX_WIDTH_OUTPUT, the image will be shrinked proportionally
	nearWhite = WHITE * THRESHOLD_MARGIN
	pixelsArr = []
	imgWidth, imgHeight = img.size

	if imgWidth > MAX_WIDTH_OUTPUT or imgHeight > MAX_HEIGHT_OUTPUT: #check if img needs to be compressed
		imgArr = [] #store the pixel of img
		compressedImgArr = [] #store the pixel of img after compression
		tmp = [] # temp array to store pixel temporary
		pixelCounter = 0
		#convert img's pixel into a 2D array
		for pixel in iter(img.getdata()):
			tmp.append(pixel)
			pixelCounter += 1
			if pixelCounter >= imgWidth:
				imgArr.append(tmp)
				tmp = [] #need to look at how python handles reassignment regarding memory management
				pixelCounter = 0
		# print("imgArr demension: ", len(imgArr), "x", len(imgArr[0]))
		#calculate the ratio the img needs to be compressed at
		compressRatio = int(round(max(imgWidth/MAX_WIDTH_OUTPUT, imgHeight/MAX_HEIGHT_OUTPUT)))
		print("compressRatio: ", compressRatio)
		#compress imgArr and put in to compressedImgArr for later process
		topLeftPixelRow = 0 #start from the first row
		btnRightPixelRow = topLeftPixelRow + compressRatio - 1
		nextBtnRightPixelRow = btnRightPixelRow
		# print("imgWidth: ", imgWidth, "imgHeight: ", imgHeight)
		while nextBtnRightPixelRow < imgHeight: #Goes through every pixel within the same row until exceeding the height of image
			topLeftPixelCol = 0 #always start from the first column
			btnRightPixelCol = topLeftPixelCol + compressRatio - 1
			nextBtnRightPixelCol = btnRightPixelCol
			while nextBtnRightPixelCol < imgWidth: #Goes through every pixel within the same column until exceeding the width of image
				currentRow = topLeftPixelRow
				currentCol = topLeftPixelCol
				#get every pixel within the group of pixels needs to be compress into one pixel
				while currentRow <= btnRightPixelRow: #goes through every pixel in row within this group
					# print("topLeftPixelRow: ", topLeftPixelRow, "topLeftPixelCol: ", topLeftPixelCol, "btnRightPixelRow: ", btnRightPixelRow, "btnRightPixelCol: ", btnRightPixelCol)
					while currentCol <= btnRightPixelCol: #goes through every pixel in column within this group
						tmp.append(imgArr[currentRow][currentCol])
						# print("CurrentRow: ", currentRow, "CurrentCol: ", currentCol)
						currentCol += 1
					currentCol = topLeftPixelCol
					currentRow += 1
				# print("GROUP!!!!!!!!!!!")
				# print("tmpList: ", tmp)
				#compress the grouped pixels into one pixel
				compressedImgArr.append(averageRGB(tmp)) #put compressed pixel in the compressedImgArr
				tmp = [] #clear tmp. need to look at how python handles reassignment regarding memory management
				#update to the next group on the right
				topLeftPixelCol += compressRatio
				btnRightPixelCol += compressRatio
				nextBtnRightPixelCol = btnRightPixelCol
				# print("Row Compressed!!!!!!!!!!!!")
			#all the groups in one single row is compress at this point

			#get the rest of the pixels on the right that are not enough to form one group
			currentRow = topLeftPixelRow
			currentCol = topLeftPixelCol
			while currentRow < btnRightPixelRow:
				while currentCol < imgWidth: #do until the currentCol is no longer with in the image's width
					tmp.append(imgArr[currentRow][currentCol])
					currentCol += 1
				currentCol = topLeftPixelCol
				currentRow += 1
			if (imgWidth/compressRatio) != int(imgWidth/compressRatio):
				#compress the last grouped pixels into one pixel
				compressedImgArr.append(averageRGB(tmp))
				tmp = [] #clear tmp
			#next row of groups
			topLeftPixelRow += compressRatio
			btnRightPixelRow = topLeftPixelRow + compressRatio
			nextBtnRightPixelRow = btnRightPixelRow
			#print("LeftOver Compressed!!!!!!!!!!!!")
			# print("tmpList: ", tmp)
		#print("nextBtnRightPixelRow: ", nextBtnRightPixelRow, "nextBtnRightPixelCol: ", nextBtnRightPixelCol)

		#tranform img to ASCII map
		pixelCounter = 0
		newImgWidth = (int(imgWidth/compressRatio) + imgWidth - (int(imgWidth/compressRatio)*compressRatio))
		for pixel in compressedImgArr:
			r,g,b = pixel
			pixelVal = r + g + b
			if pixelVal < nearWhite:
				tmp.append("M ")
			else:
				tmp.append("  ")
			pixelCounter += 1
			if pixelCounter == newImgWidth:
				pixelsArr.append(tmp)
				tmp = []
				pixelCounter = 0
		print("newImgWidth: ", newImgWidth)

	else: #img does not need to be compressed
		tmp = []
		pixelCounter = 0
		for pixel in iter(img.getdata()):
			r,g,b = pixel
			pixelVal = r + g + b
			if pixelVal < nearWhite:
				tmp.append("M ")
			else:
				tmp.append("  ")
			pixelCounter += 1
			if pixelCounter == imgWidth:
				pixelsArr.append(tmp)
				tmp = []
				pixelCounter = 0
	return pixelsArr

def printOutputImgArr(imgArr, outputFile): #write the 2D array to outputFile
	for i in range(len(pixArr)):
		for j in range(len(pixArr[i])):
			outputFile.write(pixArr[i][j])
		outputFile.write("\n")
		outputFile.flush()
	outputFile.write("/")

def shrinkImgArr(imgArr): #not used
	newArr = []
	k = 0
	i = 0
	while i < len(imgArr) - 1:
		newArr.append([])
		j = 0
		while j < len(imgArr[i]) - 1:
			newArr[k].append(imgArr[i][j])
			j += 2
		i += 2
		k += 1
	return newArr

def averageRGB(pixelList): #return a RGB tuple that contains the average of all the RGB tuples in pixelList. pixelList cannot be empty
	sumPixel = sumRGB(pixelList)
	averagePixel = sumPixel[0] / len(pixelList), sumPixel[1] / len(pixelList), sumPixel[2] / len(pixelList)
	return averagePixel

def sumRGB(pixelList): #return a RGB tuple that contains the sum of all the RGB tuples in pixelList
	sumRed, sumGreen, sumBlue = 0, 0, 0
	red, green, blue = 0, 0, 0

	for pixel in pixelList:
		red, green, blue = pixel
		sumRed += red 
		sumGreen += green
		sumBlue += blue
	
	sumPixel = sumRed, sumGreen, sumBlue
	return sumPixel

#main
#work best with square images. As the retangle ratio gets bigger, the output will look more distorted
f = open('asciiArt.txt', 'w')
img = Image.open("crunch.jpg")
pixArr = imgToArr(img)
print("pixArr dimension:", len(pixArr), len(pixArr[0]))
printOutputImgArr(pixArr, f)
f.close()
