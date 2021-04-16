import inspect
import importlib
from os import path

listOfStandAloneFunctions = []
listOfClasses = []
listOfMethodsInAClass = {}
temp = []

# Lists of Functions that need to be tested because of dependency
testDependencySets = set()

def isFunctionHeader(block) -> bool:
	if(block[0:3] == "def"):
		return True
	return False

def checkStandAloneFuncs(path):
	file = open(path)
	file = file.readlines()

	for lineNum, block in enumerate(file):
		  if(isFunctionHeader(block)):
		    index = 0
		    for char in block:
		    	if(char == "("):
		    		break
		    	index += 1
		    listOfStandAloneFunctions.append(block[4:index]) 
   	
def isClassHeader(block) -> bool:
	if(block[0:5] == "class"):
		return True;
	return False;

def checkForClasses(path):
	file = open(path)
	file = file.readlines()

	for lineNum, block in enumerate(file):
		if(isClassHeader(block)):
		    className = block[6:-2]
		    listOfClasses.append(className)

# Checks if there are dependancy insides functions
def checkForSAFuncsDependency(module):
	for function in listOfStandAloneFunctions:
		print("-----------------------------")
		print("Function called is: ", function)
		funcObj = getattr(module, function)
		blocks = inspect.getclosurevars(funcObj)
		for instruction in blocks[1]:
			if(instruction in listOfStandAloneFunctions):
				testDependencySets.add(function)
				testDependencySets.add(instruction)
				print(function, "is dependent on", instruction)						# For Debugging purposes

def checkMethodsInsideClass(module):
	for class_ in listOfClasses:
		classObj = getattr(module, class_)
		classMethodsSet = inspect.getmembers(classObj, inspect.isfunction)
		listOfMethodsInAClass[class_] = classMethodsSet

def extractMethodsFromSet(ArraysOfSet) -> [str]:

	temp.clear()

	for set_ in ArraysOfSet:
		temp.append(set_[0])

	return temp

def checkForDependencyinMethodsClass(module):
	for className, methodSet in listOfMethodsInAClass.items():
		print("-----------------------------")
		print("Class called is: ", className)
		for nameMethod, objMethod in methodSet:
			blocks = inspect.getclosurevars(objMethod)
			for instruction in blocks[3]:
				methods = extractMethodsFromSet(listOfMethodsInAClass[className])
				if(instruction in methods):
					testDependencySets.add(className + "." + nameMethod)
					testDependencySets.add(className + "." + instruction)
					print(nameMethod, "is dependent on", instruction)					# For Debugging purposes

def main():

	############## INPUT ############################
	inputPath = input('Please enter the path of the file: ')

	if(not path.exists(inputPath)):
		print("File does not exists")
		return

	print("Currently Scanning........")
	spec = importlib.util.spec_from_file_location("placeHolder", inputPath)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)

	############## FOR STANDALONE FUNCTIONS ONLY ############################
	checkStandAloneFuncs(inputPath)
	checkForSAFuncsDependency(module)

	############## FOR CLASSES FUNCTIONS ONLY ############################
	checkForClasses(inputPath)
	checkMethodsInsideClass(module)
	checkForDependencyinMethodsClass(module)

	print("---------------------------------------------")
	print("Here are the methods that need to be tested: ")
	print(testDependencySets)

	############ Insert Regression Testing Below with testDependencySets #########################
				    		
if __name__ == "__main__":
    main()