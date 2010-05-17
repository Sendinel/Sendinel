def disable_authentication(testfunc):
    def do_disable_authentication(instance, *args, **kwargs):
        from sendinel.backend import authhelper
        original_value = authhelper.AUTHENTICATION_ENABLED
        
        authhelper.AUTHENTICATION_ENABLED = False
        return_value = testfunc(instance, *args, **kwargs)
        
        authhelper.AUTHENTICATION_ENABLED = original_value
        
        return return_value

    return do_disable_authentication
