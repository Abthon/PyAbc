__author__ = "Abenezer Walelign"

import types


class AbstractBaseClass(type):
	def __new__(meta,clssName,basses,attr):
		meta.abstractMethods = []
		funcObj,isTrue = meta.validateFunction(meta,attr)

		if (isTrue):
			meta.abstractClass = type(clssName,basses,attr)
			setattr(meta.abstractClass, "__new__",meta.constractor)
			return meta.abstractClass
		else:
			raise Exception(f'{funcObj.__code__.co_name} was inmpelented!')


	def emptyFunc(meta):
		pass


	def emptyFuncWithDocString(meta):
		"test Doc String"


	def validateFunction(meta,attr):
		isValid : int = False
		funcObj : types.FunctionType = None

		for key,value in attr.items():
			if type(value) == types.FunctionType:
				if value.__code__.co_name != "wrapper":
					meta.abstractMethods.append(value.__code__.co_name)
				if value.__code__.co_code == meta.emptyFunc.__code__.co_code or value.__code__.co_code == meta.emptyFuncWithDocString.__code__.co_code or value.__code__.co_name == "wrapper":
					isValid = True
					funcObj = value
				else:
					return value,False

		return funcObj,isValid


	def preventInstantiation(meta):
		if meta == AbstractBaseClass.abstractClass:
			raise Exception(f'''
				"{meta.__name__}" is abstractClass; cannot be instantiated!		
				''')
		else:
			return True

	def getSubClassMethods(meta):
		subClassMethods = []
		for key,value in meta.__dict__.items():
			if type(value) == types.FunctionType:
				subClassMethods.append(key)

		return subClassMethods


	def validateSubClass(meta):
		isValid = True
		subClassMethods = AbstractBaseClass.getSubClassMethods(meta)
		unImplementedMethods = []
		for methods in AbstractBaseClass.abstractMethods:
			if methods not in subClassMethods:
				unImplementedMethods.append(methods)
				isValid = False

		if not (isValid):
			NotImplementeds = ",".join([methods for methods in unImplementedMethods])
			raise Exception(f"{meta.__name__} is not an abstract class and doesn't implement these functions too :- {NotImplementeds}")


	def constractor(meta):
		AbstractBaseClass.preventInstantiation(meta) 
		AbstractBaseClass.validateSubClass(meta)
		return meta

	def default(meta):
		def wrapper(*args,**kwargs):
			meta()
		return wrapper



###  ------ ###
###  USAGE  ### ---->>
###  ------ ###      ||
#                    \/


# Test Abstract class
class Test(metaclass=AbstractBaseClass):
	x : int = 4
	y : int = 6 

	def test(self,test1,test2):
		"Hello world"
		pass

	def func2(self):
		pass

	@AbstractBaseClass.default
	def default():
		print("default has body!")


# t = Test() # This doesn't work since it is not possible to create an instance for abstract classes

class SubClass1(Test):
	def test():
		pass


	def func2():
		pass



class SubClass2(SubClass1):
	pass


s1 = SubClass1() # This Works 
s1.default() # outPut --> default has body
# s2 = SubClass2() # This doesn't works
