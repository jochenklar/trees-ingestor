trees ingestor
==============

Step 1: obtain `re_anlagenbaeume.gml` and `re_strassenbaeume.gml` from the FIS broker or somewhere else.

Step 2: convert to geojson and to the WGS84 system using `gdal`:

```
ogr2ogr -s_srs EPSG:25833 -t_srs WGS84 -f geoJSON re_anlagenbaeume.json re_anlagenbaeume.gml
ogr2ogr -s_srs EPSG:25833 -t_srs WGS84 -f geoJSON re_strassenbaeume.json re_strassenbaeume.gml
```

Step 3: create a trees database

```
createdb trees
```

Step 3: generate the CREATE TABLE script and create the table.

```
cd trees-ingestor/postgres
postgres/generate-create-table-stmt.py
psql trees < create-trees.sql
```

Step 4: generate the INSERT scripts and insert the data.

```
postgres/generate-ingest-stmt.py path/to/re_anlagenbaeume.json 1
postgres/generate-ingest-stmt.py path/to/re_strassenbaeume.json 2
psql trees < insert-re_anlagenbaeume.sql
psql trees < insert-re_strassenbaeume.sql
```
