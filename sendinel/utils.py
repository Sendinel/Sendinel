def last(model):
    """
    Return the object of the given model that was last saved in the database.
    @params:model, a Class name
    """
    return model.objects.order_by("id").reverse()[:1][0]