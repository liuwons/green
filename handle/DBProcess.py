# coding: utf-8
import csv


def checkDB():

	DBResult = []

	with open('list.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ')
		for row in reader:
			if row[1] == '0':
				DBResult.append(row)
			elif row[1] == '1':
				DBResult.append(row)
			elif row[1] == '*':
				DBResult.append(row)
			else:
				return 2 #list.csv error,the status flag must be 1, 0 or *
	print DBResult
	return DBResult


def changeDB(arg, num):	#Caution!!! arg and num are all String!

	newCSVList = []
	oldCSVList = checkDB()
	if oldCSVList == 2:
		return 2 #list.csv error,the status flag must be 1, 0 or *

	for i in range(len(oldCSVList)):
		if oldCSVList[i][0] == num:
			newRow = oldCSVList[i]
			newRow[1] = arg
			newCSVList.append(newRow)
		else:
			newCSVList.append(oldCSVList[i])
	#rewrite the list.csv
	with open('list.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=' ')
		writer.writerows(newCSVList)

	return 0


def borrowEquipment(num):#Caution!!! num is a string!
	DBList = checkDB()
	if DBList == 2:
		return 2

	order = 999 #the order of the equipment in the DBList

	for i in range(len(DBList)):
		if DBList[i][0] == num:
			order = i
			break

	if order == 999:
		return 'The equipment number does not exsist'

	if DBList[order][1] == '0':
		return 'The equipment has been lent out.' #if the equipment has been lent out, return this to show the error
	elif DBList[order][1] == '1':
		if changeDB('0', num) == 0:
			return 'Succeed!' # succeed
	else:
		return 2 #list.csv error(the status flag must be 1, 0 or *), return 2 to show the error


def returnEquipment(num):#Caution!!! num is a string!
	DBList = checkDB()
	if DBList == 2:
		return 2 #list.csv error,the status flag must be 1, 0 or *

	order = 999 #the order of the equipment in the DBList

	for i in range(len(DBList)):
		if DBList[i][0] == num:
			order = i
			break
	if order == 999:
		return 'The equipment number does not exsist'

	if DBList[order][1] == '1':
		return 'The equipment hasn\'t been lent out.' #if the equipment has not been lent out, return this to show the error
	if DBList[order][1] == '0':
		if changeDB('1', num) == 0:
			return 'Succeed!' # succeed


def showEquipment():
	DBList = checkDB()
	if DBList == 2:
		return 2 #list.csv error,the status flag must be 1, 0 or *

	returnString = ''
	for i in range(len(DBList)):
		if DBList[i][1] == '1':
			returnString += DBList[i][2]
			returnString += ' Available\n'
		elif DBList[i][1] == '0':
			returnString += DBList[i][2]
			returnString += ' Unavailable\n'
		else:
			returnString += '***'
			returnString += DBList[i][2]
			returnString += '***\n'

	return returnString

#print(checkDB())
#print(borrowEquipment('101'))
#print(checkDB())
#print(returnEquipment('101'))
#print(checkDB())
#print(showEquipment())
