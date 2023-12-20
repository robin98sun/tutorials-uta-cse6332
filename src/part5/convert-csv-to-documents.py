#!/usr/bin/env python3
import csv, os, json, argparse, shutil, time

parser = argparse.ArgumentParser(description='Convert a CSV file into a collection of JSON documents')

parser.add_argument(
    '--csv-file', type=str, required=False,
    help='the CSV file to be converted, the header line MUST be at the first line in the file'
)

parser.add_argument(
    '--output-dir', type=str, required=False, default='coll',
    help='the directory to store the generated JSON documents'
)

parser.add_argument(
    '--db-conn-str', type=str, required=False,
    help='the database connection string of an Azure Cosmos DB instance'
)

parser.add_argument(
    '--db-name', type=str, required=False,
    help='the database name'
)

parser.add_argument(
    '--table-name', type=str, required=False,
    help='the table name'
)

parser.add_argument(
    '--id-name', type=str, required=False,
    help='the name for the id of each record'
)

parser.add_argument(
    '--start-row', type=int, required=False, default = 0,
    help='from which row of the csv file to start reading' 
)
parser.add_argument(
    '--lines', type=int, required=False, default = 0,
    help='the total lines of the csv file to read from the starting row'
)

args = parser.parse_args()

from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient

db, id_name = None, "item"
if args.db_conn_str is not None and args.db_name is not None and args.table_name is not None:
    db_client = CosmosClient.from_connection_string(conn_str = args.db_conn_str)
    db = db_client.get_database_client(args.db_name)
    if args.id_name is not None:
        id_name = args.id_name

with open(args.csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    row_id = -1
    headers = []
    
    if db is None:
        if os.path.exists(args.output_dir):
            shutil.rmtree(args.output_dir)
        os.mkdir(args.output_dir)

    lines_to_read = -1
    if args.lines > 0:
        lines_to_read = args.lines
    start_row = args.start_row

    for row in csvreader:
        row_id+=1
        doc = {}
        col_id = -1
        for raw_col in row:
            col_id += 1
            col = raw_col.replace('"', '')
            if row_id == 0:
                headers.append(col)
            elif col_id >= len(headers):
                continue
            else:
                col_name = headers[col_id] 
                doc[col_name] = col

        if row_id > start_row and lines_to_read > 0:
            lines_to_read-=1
            if db is None:
                doc_name = "doc-{}".format(row_id)
                doc_path = "{}/{}.json".format(args.output_dir, doc_name)
                with open(doc_path, 'w') as docfile:
                    json.dump(doc, docfile, indent=4)
                    docfile.close()
            elif db is not None:
                doc["id"] = "{}-{}".format(id_name, row_id)
                container = db.get_container_client(args.table_name)
                res = container.upsert_item(doc)
            
            if args.lines > 0:
                if row_id % 50 == 0:
                    print(".{:.3f}%".format(row_id/(args.lines+args.start_row) * 100), end="", flush=True)
                else:
                    print(".", end="", flush=True)
                    
    csvfile.close()
    print("done")




