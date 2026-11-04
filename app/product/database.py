from pathlib import Path
from tinydb import TinyDB, Query


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / 'data'
    / 'products.json'
)

DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

db = TinyDB(
    DATA_FILE,
    ensure_ascii=False,
    indent=2
)

products_table = db.table('products')
ProductQuery = Query()


def next_product_id(table=None):
    table = table if table is not None else products_table

    return max(
        (item.get('id', 0) for item in table.all()),
        default=0
    ) + 1