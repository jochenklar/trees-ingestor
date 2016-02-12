#!/usr/bin/env python

import argparse
import json
import os
import sys

from settings import SCHEMA

parser = argparse.ArgumentParser(description='Generates the INGEST statements.')
parser.add_argument('file', action='store', help='the geojson file with the data')
parser.add_argument('type_id', action='store', help='the type_id to be stored in the database')
args = parser.parse_args()

filename = 'insert-' + os.path.basename(args.file).replace('json', 'sql')
f = open(filename, 'w')

f.write('INSERT INTO trees (%s) \nVALUES \n' % ', '.join(field['name'] for field in SCHEMA))

geojson_dict = json.loads(open(args.file).read())

for feature in geojson_dict['features']:

    insert_stmt = '('
    insert_stmt += str(feature['geometry']['coordinates'][0]) + ', '  # lat
    insert_stmt += str(feature['geometry']['coordinates'][1]) + ', '  # lon

    for field in SCHEMA[2:-1]:  # skip lat and lon and type_id
        if field['name'] in feature['properties']:
            value = feature['properties'][field['name']]

            if value is None:
                string = 'NULL'
            elif field['type'].startswith('varchar'):
                string = "'" + value.replace("'", '"') + "'"
            else:
                string = str(value)
        else:
            string = 'NULL'

        insert_stmt += string + ', '

    insert_stmt += str(args.type_id) + ')'  # type_id

    if feature != geojson_dict['features'][-1]:
        insert_stmt += ',\n'

    f.write(insert_stmt.encode('utf8'))

f.write(';')
