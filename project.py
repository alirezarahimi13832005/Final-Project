import cv2
import json
import math
import numpy as np

##################
#Alireza Rahimi
##################


##################
#صفحه انتخاب مسئله
##################
def main_scr():
	choice = int(input("1.convolution\n2.quidditch\n3.smart attendance\n4.wiring\n\n>> "))
	if choice == 1:
		q1()
	elif choice == 2:
		q2()
	elif choice == 3:
		q3()
	elif choice == 4:
		q4()
	else:
		print("wrong input")
		main_scr()


##################
#تابع کانوولوشن
##################
def conv(signal, filter):
	result = [0] * (len(signal) + len(filter) - 1)
	
	for i in range(len(signal)):
		for j in range(len(filter)):
			result[i + j] += signal[i] * filter[j]
	
	return result

##################
#تابع کانوولوشن غیر خطی
##################
def conv2d(image, filter):
	hF, wF = filter.shape
	hI, wI = image.shape
	
	res = np.zeros((hI, wI))
	
	padded_image = np.pad(image, ((hF // 2, hF // 2), 
								  (wF // 2, wF // 2)), mode='constant')
	
	for i in range(hI):
		for j in range(wI):
			region = padded_image[i:i + hF, j:j + wF]
			res[i, j] = np.sum(region * filter)
	
	return res
	
##################
#مسئله 1
##################
def q1():
	s = []
	f = []
	lenS = int(input("what is signal length? >> "))

	for i in range(0, int(lenS)):
		s.append(input(f"{i+1} >>"))

	lenF = int(input("what is filter length? >> "))

	for i in range(0, int(lenF)):
		f.append(input(f"input the {i+1} member of filter: "))

	for i in range(0, len(s)):
		s[i] = int(s[i])

	for i in range(0, len(f)):
		f[i] = int(f[i])

	res = conv(s, f)
	print(f"{res}")

	result = {
		"q_num": 1,
		"q_ans": res
	}

	with open("history.txt", "a") as file:
		file.write(f"{json.dumps(result)}\n")

##################
#مسئله 2
##################
def q2():
	row = int(input("number of rows >> "))
	col = int(input("number of cols >> "))
	
	x = 0
	y = 0
	
	target = 0

	targetRow = 0
	targetCol = 0

	arr = [[0 for x in range(int(col))] for y in range(int(row))]

	for i in range(0, row):
		for j in range(0, col):
			arr[i][j] = input(f"{i+1} {j+1} >> ")
			if arr[i][j] == "o" or arr[i][j] == "O":
				target = 1
				targetRow = i
				targetCol = j
			
	if targetRow == -1 or targetCol == -1:
		print("There was no target")
		main_scr()

	for i in range(0, row):
		for j in range(0, col):
			if i == targetRow and j == targetCol:
				continue
			else:
				radius = math.sqrt((i - targetRow) **2 + (j - targetCol) **2)
				if radius == 0:
					continue
				p_e = int(arr[i][j]) / (radius **2)
				x += p_e * ((i - targetRow) / radius)
				y += p_e * ((j - targetCol) / radius)

	
	print(f"\nK*({x}i + {y}j)")
	
	result = {
		"q_num": 2,
		"input" : arr,		
		"res": {
			"x" : x,
			"y" : y
		}
	}

	with open("history.txt", "a") as file:
		file.write(f"{json.dumps(result)}\n")

##################
#مسئله 3
##################
def q3():
	name = "C:\\Users\\P.Andishe\\Desktop\\New folder (4)\\uni.webp"

	image = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
	image_array = np.array(image)

	xFilter = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

	yFilter = np.array([[-1, -2, -1],
						[ 0,  0,  0],
						[ 1,  2,  1]])

	edge_x = conv2d(image_array, xFilter)
	edge_y = conv2d(image_array, yFilter)

	edges = np.hypot(edge_x, edge_y)
	edges = edges / edges.max() * 255

	cv2.imwrite(".\\history.png", edges.astype(np.uint8))
	cv2.imshow('Edges', edges.astype(np.uint8))
	cv2.waitKey(0)
	cv2.destroyAllWindows()

##################
#مسئله 4
##################
def q4():
	power = float(input("watt >> "))
	Density = float(input("A/CM **2 >> "))
	v1 = float(input("primart V >> "))
	v2 = float(input("secondary V >> "))

	area = round(power / (Density * v2), 4)

	round1 = round(v1 / math.sqrt(2), 4)
	round2 = round(v2 / math.sqrt(2), 4)

	print(f"area of core >> {area}")
	print(f"first round >> {round1}")
	print(f"second round >> {round2}")

	result = {
		"q_num": 4,
		"res": {
			"core_area": area,
			"primary_rounds": round1,
			"secondary_rounds": round2
		}
	}

	with open("history.txt", "a") as file:
		file.write(f"{json.dumps(result)}\n")

main_scr()