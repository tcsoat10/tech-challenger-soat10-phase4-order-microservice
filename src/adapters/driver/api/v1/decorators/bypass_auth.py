def bypass_auth():
    """
    Decorator para adicionar o atributo `bypass_auth` ao endpoint.
    """
    
    def decorator(func):
        if not hasattr(func, "bypass_auth"):
            func.bypass_auth = True
        return func
    return decorator