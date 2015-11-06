class MetaSingleton(type):
    # instance = None
    def __new__(mcs, *t, **d):
        if __name__ == "__main__" :
            print("NEW METACLASS")
        return super().__new__(mcs, *t, **d)

    def __init__(cls, *t, **d):
        if __name__ == "__main__" :
            print("INIT METACLASS", cls)
        super().__init__(*t, **d)
        cls.instance = None
        pass
    
    def __call__(cls, *t, **d):
        if __name__ == "__main__" :
            print("CALL METACLASS", cls)
        if cls.instance is None :
            cls.instance = super().__call__(*t, **d)
        return cls.instance
    
    pass

if __name__ == "__main__" :
    class MonSingleton(object, metaclass=MetaSingleton):

        attribut = "Atribut"

        def __new__(cls, *t, **d):
            print("NEW MaCLASS")
            return super().__new__(cls, *t, **d)

        def __init__(self, *t, **d):
            print("INIT MaCLASS")
            super().__init__(*t, **d)
            pass

        def __call__(self,*t, **d):
            print("CALL maCLASS")
            return super().__call__(*t, **d)

        pass


    class Single2(object, metaclass=MetaSingleton):
        pass


    class Single3(object, metaclass=MetaSingleton):
        pass

    s1 = MonSingleton()
    print("INSTANCE ", s1.instance)
    assert( s1 == s1.instance)
    print(s1)
    s2 = MonSingleton()
    print(s2)
    assert(id(s1) == id(s2))

    s3 = Single2()
    print(s3)
    s4 = Single2()
    print(s4)
    assert(id(s3) == id(s4))
    assert(id(s1) != id(s3))

    s5 = Single3()
    print(s5)
    s6 = Single3()
    print(s6)
    assert(id(s5) == id(s6))
    assert(id(s1) != id(s5))
    assert(id(s3) != id(s5))