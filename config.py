#!/usr/bin/python3.10


from configparser import ConfigParser


def config(filename='./config/config.ini', section='employee_ids'):
    parser = ConfigParser()
    parser.read(filename)

    api_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            api_params[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return api_params
