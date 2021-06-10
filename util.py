from constant import dbs_type_list, dom_type_list


def toPascalCase(str):
    return str[0].upper() + str[1:]


def databaseTypeValidation(type_list):
    if not all(item in dbs_type_list for item in type_list):
        raise Exception("Unknown Variable Type.")


def domainTypeValidation(type_list):
    if not all(item in dom_type_list for item in type_list):
        raise Exception("Unknown Variable Type.")
