def render_sort(instance_list, camera, *types):
    _visible_instance_list = [] 
    
    for instance in instance_list:
        if not instance.get_out_of_view(camera) or instance.type == "Beam":
            _visible_instance_list.append(instance)
            
    return _visible_instance_list