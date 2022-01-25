

def json_to_listview(json_data, keys):
    '''
    Changes json object to array (ListView format) for google sheets entry.

    :param json_data: json object for parsing.
    '''
    json_to_list = [[k for k in keys]]
    if json_data == 0 or json_data:
        if isinstance(json_data, list):
            for obj in json_data:
                json_to_list.append(json_to_listview(obj, keys))
            return json_to_list

        elif isinstance(json_data, dict):
            dict_to_list = []
            for k in keys:
                try:
                    v = json_data[k]
                except KeyError:
                    v = ''
                if isinstance(v, list):
                    v = [str(i) for i in v]
                    v_str = ','.join(v)
                    dict_to_list.append(v_str)
                else:
                    dict_to_list.append(str(v))
            # TODO: unpack values?
            # TODO: check if headers exist
            return dict_to_list
        return json_data
