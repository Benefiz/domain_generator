import os
import io
import constant
from util import toPascalCase


def daoGenerator(dao_type_list, dao_name_list, domain_name_list, class_name, table_name):
    if(len(dao_name_list) != len(dao_type_list)):
        raise Exception("Unequal length.")
    var_lines = []
    mapper_object_lines = []
    for i, type in enumerate(dao_type_list):
        var_lines.append(var_convert(dao_name_list[i]))
        mapper_object_lines.append(mapper_object_convert(
            dao_type_list[i], dao_name_list[i], domain_name_list[i]))
    # Create DaoImpl
    dao_impl_template = replace_dao_impl_attribute(
        var_lines, mapper_object_lines, table_name, class_name, constant.author)
    file_name = os.path.join(constant.project_path, constant.package_path,
                             constant.dao_impl_path, class_name+'DaoImpl.java')
    file = io.open(file_name, "w", encoding="utf-8")
    file.writelines(dao_impl_template)
    file.close()
    # Create Dao
    dao_template = replace_dao_attribute(class_name, constant.author)
    file_name = os.path.join(constant.project_path, constant.package_path,
                             constant.dao_path, class_name+'Dao.java')
    file = io.open(file_name, "w", encoding="utf-8")
    file.writelines(dao_template)
    file.close()
    print("Success : Create dao completed.")


def var_convert(name):
    return '\tprivate final String {} = "{}";\n'.format(name.upper(), name)


def mapper_object_convert(dao_type, dao_name, domain_name):
    s = ""
    if dao_type == 'varchar':
        s = "\t\tmapperObject.set{domain}(rs.getString({dao}));\n"
    elif dao_type == 'bigint':
        s = "\t\tmapperObject.set{domain}(rs.getObject({dao}) != null ? BigInteger.valueOf(rs.getLong({dao})) : null);\n"
    elif dao_type == 'datetime':
        s = "\t\tmapperObject.set{domain}(rs.getTimestamp({dao}));\n"
    elif dao_type == 'int':
        s = "\t\tmapperObject.set{domain}(rs.getObject({dao}) != null ? rs.getInt({dao}) : null);\n"
    else:
        raise Exception("Unknown Variable Type.")
    return s.format(domain=toPascalCase(domain_name), dao=dao_name.upper())


def replace_dao_impl_attribute(var_lines, mapper_object_lines, table_name, domain_name, author):
    return open('template/dao_impl_template.txt', 'r').read().format(
        var="".join(var_lines), mapper_object="".join(mapper_object_lines),
        table=table_name, domain=domain_name, author=author, package_dao=constant.dao_path.replace(
            '/', '.'),
        package_domain=constant.domain_path.replace('/', '.'))


def replace_dao_attribute(domain_name, author):
    return open('template/dao_template.txt', 'r').read().format(
        domain=domain_name, author=author, package=constant.dao_path.replace('/', '.'))
