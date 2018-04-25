def pytype(*type_args,**type_kwargs):
    """
    Check a function's arguments for expected types
    """
    # Determine if the given type is an iterable
    def is_iter(type_):
        return "__iter__" in dir(type_)
    # Convert any non iterable arguments to lists of element one for consistency
    type_args = [arg if is_iter(arg) else [arg] for arg in type_args]
    # Do the same for keyword args
    new_kwargs = {}
    for name,type_set in type_kwargs.items():
        new_kwargs[name] = type_set if is_iter(type_set) else [type_set]
    type_kwargs = new_kwargs

    def _pytype(func):
        nonlocal type_args
        nonlocal type_kwargs
        # Create a dict of varname to possible types
        varnames = func.__code__.co_varnames
        types_ = dict(zip(varnames,type_args))
        types_.update(type_kwargs)
        def wrapped_func(*args,**kwargs):
            def any_type_in(possible_types,target_type):
                return any(t == tt for t in possible_types 
                                    for tt in target_type.__mro__)
            nonlocal types_
            nonlocal varnames
            nonlocal func
            # Create a dict of varname to given value
            values = dict(zip(varnames,args))
            values.update(kwargs)
            # All argument values must match up to the possible types given
            for name,value in values.items():
                assert any_type_in(types_[name],type(value)),"{} must be one of types {} it actually is {}!".format(name,types_[name],type(value))
            result = func(*args,**kwargs)
            return result 
        return wrapped_func
    return _pytype

if __name__ == "__main__":
    class A:
        pass
    class B(A):
        pass

    @pytype(A,A)
    def inheritance_check(a,b):
        print("Inheritance is now checked")
        return True
    inheritance_check(B(),A())

    class HasAttr:
        def __init__(self,attr):
            self.attr = attr
        def __eq__(self,other):
            return self.attr in dir(other)

    @pytype(HasAttr("__iter__"),int)
    def window(iterable,size):
        return list(zip(*([iter(iterable)]*size)))

    print(window(range(14),5))
    # window(1,2) -- raises exception

    @pytype(int,int)
    def add(a,b):
        return a + b
    print(add(1,2))
    try:
        add(1.0,2.0)
    except Exception as e:
        print("Type Error:",e)
