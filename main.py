import os
import pandas as pd
import constant
import dao_generator as dag
import domain_generator as dog
import regex as re
import util

if __name__ == '__main__':
    for file in [file for file in os.listdir("input") if file.endswith('.csv')]:
        csv = pd.read_csv("input/"+file)
        class_name = re.split('\-|\.',file)[0]
        table_name = re.split('\-|\.',file)[1]
        dom_type = csv['dom_type']
        dom_name = csv['dom_name']
        dao_type = csv['dao_type']
        dao_name = csv['dao_name']
        # Validate variable type
        util.databaseTypeValidation(dao_type)
        util.domainTypeValidation(dom_type)
        print("Domain name : ",class_name)
        print("Table name : ",table_name)
        if(constant.createDomain):
            print("Creating domain...")
            dog.domainGenerator(dom_type,dom_name,class_name)
        if(constant.createDao):
            print("Creating dao...")
            dag.daoGenerator(dao_type,dao_name,dom_name,class_name,table_name)