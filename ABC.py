__author__ = "Abenezer Walelign"
import types


class PyAbstractBaseClass(type):
    def __new__(meta, clssName, basses, attr):
        attr["__meta__"] = True
        meta.abstractMethods = []
        funcObj, isTrue = meta.validateFunction(meta, attr, basses)

        if (isTrue):
            meta.abstractClass = type(clssName, basses, attr)
            setattr(meta.abstractClass, "__new__", meta.constractor)
            return meta.abstractClass

        elif (funcObj is None and not (isTrue)):
            meta.abstractClass = type(clssName, basses, attr)
            setattr(meta.abstractClass, "__new__", meta.constractor)
            return meta.abstractClass

        else:
            raise Exception(f'{funcObj.__code__.co_name} was inmpelented!')

    def AddAbstractMethods(meta, basses):
        """ """
        PyAbstractBaseClass.abstractMethods.clear()
        if len(basses) > 0:
            for basse in basses:
                try:
                    if basse.__meta__:
                        PyAbstractBaseClass.abstractMethods.extend(
                            PyAbstractBaseClass.getAbstractClassMethods(meta, basse))
                except:
                    pass

    def getAbstractClassMethods(meta, basse):
        """ """
        abstractMethods = []
        for key, value in basse.__dict__.items():
            if type(value) == types.FunctionType:
                if (value.__code__.co_code == PyAbstractBaseClass.emptyFunc.__code__.co_code or value.__code__.co_code == PyAbstractBaseClass.emptyFuncWithDocString.__code__.co_code):
                    abstractMethods.append(key)
        return abstractMethods

    def emptyFunc(meta):
        pass

    def emptyFuncWithDocString(meta):
        "test Doc String"

    def validateFunction(meta, attr, basses):
        """ """
        
        isValid: "int" = False
        funcObj: types.FunctionType = None

        for key, value in attr.items():
            if type(value) == types.FunctionType:
                if value.__code__.co_name != "wrapper":
                    # meta.abstractMethods.append(value.__code__.co_name)
                    meta.AddAbstractMethods(meta, basses)

                if value.__code__.co_code == meta.emptyFunc.__code__.co_code or value.__code__.co_code == meta.emptyFuncWithDocString.__code__.co_code or value.__code__.co_name == "wrapper":
                    isValid = True
                    funcObj = value
                else:
                    return value, False

        return funcObj, isValid

    def preventInstantiation(meta):
        """ """
        if meta == PyAbstractBaseClass.abstractClass:
            raise Exception(f'''
				"{meta.__name__}" is abstractClass; cannot be instantiated!		
				''')
        else:
            return True

    def getSubClassMethods(meta):
        """ """
        subClassMethods = []
        for key, value in meta.__dict__.items():
            if type(value) == types.FunctionType:
                subClassMethods.append(key)

        return subClassMethods

    def validateSubClass(meta):
        """ """
        isValid = True
        subClassMethods = PyAbstractBaseClass.getSubClassMethods(meta)
        unImplementedMethods = []
        PyAbstractBaseClass.AddAbstractMethods(meta, meta.mro())
        for methods in PyAbstractBaseClass.abstractMethods:
            if methods not in subClassMethods:
                unImplementedMethods.append(methods)
                isValid = False

        if not (isValid):
            NotImplementeds = ",".join(
                [methods for methods in unImplementedMethods])
            raise Exception(
                f"{meta.__name__} is not an abstract class and doesn't implement these functions :- {NotImplementeds}")

    def constractor(meta):
        """ """
        PyAbstractBaseClass.preventInstantiation(meta)
        PyAbstractBaseClass.validateSubClass(meta)
        return meta

    def default(meta):
        """ """
        def wrapper(*args, **kwargs):
            meta(*args, **kwargs)
        return wrapper




### ------ ###
#   USAGE  ### ---->>
# -------- ###      ||
#                   \/


# Test Abstract class
class Test(metaclass=PyAbstractBaseClass):
    x: int = 4
    y: int = 6

    def test(self, test1, test2):
        "Hello world"
        pass

    def func2(self):
        pass

    @PyAbstractBaseClass.default
    def default(a, b, *, c, d):
        print("default has body!")


# t = Test() # This doesn't work since it is not possible to create an instance for abstract classes

class SubClass1(Test):
    pass


class SubClass2(Test, metaclass=PyAbstractBaseClass):
    def newAbstractMethod():
        pass


class SubClass3(SubClass2):
    pass


class SubClass4(Test):
    def test(self):
        pass

    def func2(self):
        pass



# s3 = SubClass3()  # This doesn't works  because it doesn't implement --> test, func2 and newAbstractMethod
# s1 = SubClass1() # This doesn't Works  because it doesn't implement  --> test, func2
s4 = SubClass4()  # works
s4.default(1, 2, c=3, d=4) # also works fine
