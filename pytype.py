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
            nonlocal types_
            nonlocal varnames
            nonlocal func
            # Create a dict of varname to given value
            values = dict(zip(varnames,args))
            values.update(kwargs)
            # All argument values must match up to the possible types given
            for name,value in values.items():
                assert type(value) in types_[name],"{} must be one of types {} it actually is {}!".format(name,types_[name],type(value))
            result = func(*args,**kwargs)
            return result 
        return wrapped_func
    return _pytype

if __name__ == "__main__":
    @pytype(int,int)
    def add(a,b):
        return a + b
    print(add(1,2))
    try:
        add(1.0,2.0)
    except Exception as e:
        print("Type Error:",e)
