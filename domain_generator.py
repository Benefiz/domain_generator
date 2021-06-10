import os
import io
import constant
from util import toPascalCase


def domainGenerator(variable_type_list, variable_name_list, class_name):
    if(len(variable_name_list) != len(variable_type_list)):
        raise Exception("Unequal length.")
    var_lines = []
    getter_setter_lines = []
    for i, type in enumerate(variable_type_list):
        var_lines.append(var_convert(
            variable_type_list[i], variable_name_list[i]))
        getter_setter_lines.append(getter_setter_convert(
            variable_type_list[i], variable_name_list[i], toPascalCase(variable_name_list[i])))
    domain_template = replace_attribute(
        var_lines, getter_setter_lines, class_name, constant.author)
    file_name = os.path.join(
        constant.project_path, constant.package_path, constant.domain_path, class_name+'.java')
    file = io.open(file_name, "w", encoding="utf-8")
    file.writelines(domain_template)
    file.close()
    print("Success : Create domain completed.")


def var_convert(type, name):
    return "\tprivate {type} {name};\n".format(type=type, name=name)


def getter_setter_convert(type, name, pascal_name):
    return open('template/getter_setter_template.txt', 'r').read().format(
        type=type, name=name, pascal_name=pascal_name, getter='is' if type.startswith('bool') else 'get')


def replace_attribute(var_lines, getter_setter_lines, domain, author):
    return open('template/domain_template.txt', 'r').read().format(
        var="".join(var_lines), getter_setter="\n\n".join(getter_setter_lines), domain=domain, author=author, package=constant.domain_path.replace('/', '.'))
