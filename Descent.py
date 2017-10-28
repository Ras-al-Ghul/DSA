def value(x):
	print ((x[0]**2)+(x[1]**2)+((x[1]**2)*(x[3]**2))+((x[1]**3)*(x[3]))+(x[2]**3)+(x[2]*x[4])-((x[2]**2)*x[4])-(x[3]*x[6])-((x[3]**2)*(x[6]**2))-((x[5]**3)*(x[7]**3))+((x[5]**2)*(x[7]**3))+(x[5]*(x[8]**2))-(x[5]**2)+(x[7]**3)+(x[7]*(x[8]**2))+(x[5]*x[9])-((x[5]**2)*(x[9]**2)))

def descent():
	arr = [1.0,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
	oldx = [1,1,1,1,1,1,1,1,1,1]
	# x = [0,0,-15,-15,15,15,-15,15,0,-15]
	x = [0,0,-30,-30,30,30,-30,30,0,-30]
	value(x)

	# x = [0.0, 0.0, -15, -15, -15, 15, -15, 15, 0.0, -15]
	counter = 0
	while True:
		ox = x[:]
		if(abs(x[0]-oldx[0]) > 0.000001):
			print "x0",(0.1*arr[counter]*(2*ox[0])),
			oldx[0] = x[0]
			x[0] = min(max(-30,oldx[0] - (0.1*arr[counter]*(2*ox[0]))),30)
		if(abs(x[1]-oldx[1]) > 0.000001):
			print "x1",(0.1*arr[counter]*((2*ox[1])+(2*ox[1]*(ox[3]**2))+(3*(ox[1]**2)*ox[3]))),
			oldx[1] = x[1]
			x[1] = min(max(-30,oldx[1] - (0.1*arr[counter]*((2*ox[1])+(2*ox[1]*(ox[3]**2))+(3*(ox[1]**2)*ox[3])))),30)
		if(abs(x[2]-oldx[2]) > 0.000001):
			print "x2",(0.1*arr[counter]*((3*(ox[2]**2))+(ox[4])-(2*ox[2]*ox[4]))),
			oldx[2] = x[2]
			x[2] = min(max(-30,oldx[2] - (0.1*arr[counter]*((3*(ox[2]**2))+(ox[4])-(2*ox[2]*ox[4])))),30)
		if(abs(x[3]-oldx[3]) > 0.000001):
			print "x3",(0.1*arr[counter]*((2*(ox[1]**2)*ox[3])+(ox[1]**3)-(ox[6])-(2*ox[3]*(ox[6]**2)))),
			oldx[3] = x[3]
			x[3] = min(max(-30,oldx[3] - (0.1*arr[counter]*((2*(ox[1]**2)*ox[3])+(ox[1]**3)-(ox[6])-(2*ox[3]*(ox[6]**2))))),30)
		if(abs(x[4]-oldx[4]) > 0.000001):
			print "x4",(0.1*arr[counter]*((ox[2])-(ox[2]**2))),
			oldx[4] = x[4]
			x[4] = min(max(-30,oldx[4] - (0.1*arr[counter]*((ox[2])-(ox[2]**2)))),30)
		if(abs(x[5]-oldx[5]) > 0.000001):
			print "x5",(0.1*arr[counter]*(-(3*(ox[5]**2)*(ox[7]**3))+(2*ox[5]*(ox[7]**3))+(ox[8]**2)-(2*ox[5])+(ox[9])-(2*ox[5]*(ox[9]**2)))),
			oldx[5] = x[5]
			x[5] = min(max(-30,oldx[5] - (0.1*arr[counter]*(-(3*(ox[5]**2)*(ox[7]**3))+(2*ox[5]*(ox[7]**3))+(ox[8]**2)-(2*ox[5])+(ox[9])-(2*ox[5]*(ox[9]**2))))),30)
		if(abs(x[6]-oldx[6]) > 0.000001):
			print "x6",(0.1*arr[counter]*(-(ox[3])-(2*(ox[3]**2)*ox[6]))),
			oldx[6] = x[6]
			x[6] = min(max(-30,oldx[6] - (0.1*arr[counter]*(-(ox[3])-(2*(ox[3]**2)*ox[6])))),30)
		if(abs(x[7]-oldx[7]) > 0.000001):
			print "x7",(0.1*arr[counter]*(-(3*(ox[5]**3)*(ox[7]**2))+(3*(ox[5]**2)*(ox[7]**2))+(3*(ox[7]**2))+(ox[8]**2))),
			oldx[7] = x[7]
			x[7] = min(max(-30,oldx[7] - (0.1*arr[counter]*(-(3*(ox[5]**3)*(ox[7]**2))+(3*(ox[5]**2)*(ox[7]**2))+(3*(ox[7]**2))+(ox[8]**2)))),30)
		if(abs(x[8]-oldx[8]) > 0.000001):
			print "x8",(0.1*arr[counter]*((2*ox[5]*ox[8])+(2*ox[7]*ox[8]))),
			oldx[8] = x[8]
			x[8] = min(max(-30,oldx[8] - (0.1*arr[counter]*((2*ox[5]*ox[8])+(2*ox[7]*ox[8])))),30)
		if(abs(x[9]-oldx[9]) > 0.000001):
			print "x9",(0.1*arr[counter]*(ox[5]-(2*(ox[5]**2)*ox[9]))),
			oldx[9] = x[9]
			x[9] = min(max(-30,oldx[9] - (0.1*arr[counter]*(ox[5]-(2*(ox[5]**2)*ox[9])))),30)

		print oldx, x
		value(x)
		oldx = ox[:]
		counter += 1
		if counter == 12:
			break
	print x

def main():
	arr = [1.0,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
	descent()
	# oldx = 2
	# x = 1
	# counter = 0
	# while abs(x-oldx) > 0.000001:
	# 	oldx = x
	# 	x = oldx - (0.1*arr[counter]*((4*oldx) - 1))
	# 	print x, oldx
	# 	counter += 1
	# 	if counter == 12:
	# 		break
	# print x
	# oldx = [2,2,2]
	# x = [-1,-1,-1]
	# counter = 0
	# while True:
	# 	if(abs(x[0]-oldx[0]) > 0.000001):
	# 		oldx[0] = x[0]
	# 		x[0] = max(-5,oldx[0] - (0.1*arr[counter]*((3*oldx[0]*oldx[0])-oldx[1]+oldx[2])))
	# 	if(abs(x[1]-oldx[1]) > 0.000001):
	# 		oldx[1] = x[1]
	# 		x[1] = max(-5,oldx[1] - (0.1*arr[counter]*(-oldx[0]-oldx[2])))
	# 	if(abs(x[2]-oldx[2]) > 0.000001):
	# 		print x,oldx, "here"
	# 		oldx[2] = x[2]
	# 		x[2] = max(-5,oldx[2] - (0.1*arr[counter]*(oldx[0]-oldx[1])))
	# 		print x,oldx, "here"
	# 	print x, oldx
	# 	counter += 1
	# 	if counter == 12:
	# 		break
	# print x

if __name__ == '__main__':
	main()