def render_sort(instance_list, camera, *types): # TODO: make it sort based off the arguments in types.
    _visible_instance_list = [] 
    
    for instance in instance_list:
        if not instance.get_out_of_view(camera) or hasattr(instance, "always_render"):
            _visible_instance_list.append(instance)
            
    return _visible_instance_list