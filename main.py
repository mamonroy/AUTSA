def main():

	############## INPUT ############################
	originalInput = input('Please enter the path of the original file: ')
	modifiedInput = input('Please enter tha path of the modified file: ')

	if(not path.exists(originalInput) or not path.exists(modifiedInput)):
		print("Files do not exists")
		return

	################ DEPENDANCY SCANNER STARTS #############################
	print("Dependency Check Starts")
	spec = importlib.util.spec_from_file_location("test", originalInput)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)

	############## FOR STANDALONE FUNCTIONS ONLY ############################
	checkStandAloneFuncs(originalInput)
	checkForSAFuncsDependency(module)

	############## FOR CLASSES FUNCTIONS ONLY ###############################
	checkForClasses(originalInput)
	checkMethodsInsideClass(module)
	checkForDependencyinMethodsClass(module)

	# print("---------------------------------------------")
	print("Here are the methods that need to be tested: ")
	print(testDependencySets,"\n\n")

	############ REGRESSION STARTS BASED ON DEPENDENCY #########################
	fileName = os.path.basename(originalInput)  				
	locationOriginal = os.path.dirname(originalInput) + "/"   		
	locationModified = os.path.dirname(modifiedInput)  + "/"

	regression.regTest(locationOriginal, locationModified, fileName , list(testDependencySets))

	# Draw the directed Graph Diagram 
	directedGraph.draw()
				    		
if __name__ == "__main__":
    main()