#!/usr/bin/env python

import argparse

from settings import SCHEMA

parser = argparse.ArgumentParser(description='Generates the CREATE TABLE statement.')
args = parser.parse_args()

filename = 'create-trees.sql'

create_table_stmt = '''
DROP TABLE IF EXISTS trees;
CREATE TABLE trees (
    id SERIAL PRIMARY KEY,
'''

for field in SCHEMA:
    create_table_stmt += '    ' + field['name'] + ' ' + field['type']
    if 'options' in field:
        create_table_stmt += ' ' + field['options']

    if field == SCHEMA[-1]:
        create_table_stmt += '\n'
    else:
        create_table_stmt += ',\n'

create_table_stmt += ');'

open('create-trees.sql', 'w').write(create_table_stmt)
