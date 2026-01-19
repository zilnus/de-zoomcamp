import click
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}

@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='postgres', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
@click.option('--chunksize', default=10000, type=int, help='Chunk size for reading Parquet')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):

#   Connection to PostgreSQL
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

#   Get Taxi Zone Data
    url = 'taxi_zone_lookup.csv'
    df_zone = pd.read_csv(url, dtype=dtype)
    df_zone.to_sql(
        name='taxi_zone_lookup',
        con=engine,
        if_exists="replace"
    )

#   Get Green Taxi Data
    url = f'green_tripdata_{year}-{month:02d}.parquet'
    pq_file = pq.ParquetFile(url)

    with tqdm(total=pq_file.metadata.num_rows, desc="Rows processed") as pbar:
        first = True
        for batch in pq_file.iter_batches(batch_size=chunksize):
            df_chunk = batch.to_pandas()
            if first:
                df_chunk.head(0).to_sql(
                    name=target_table,
                    con=engine,
                    if_exists="replace"
                )
                first = False
                print("Table created")

            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="append"
            )
            print("Inserted:", len(df_chunk))
            pbar.update(len(df_chunk))



if __name__ == '__main__':
    run()