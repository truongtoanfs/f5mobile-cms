from models import ProductCreate, Product
from celery_config import app
from dependencies import get_db


@app.task
def writeDb(products: list[ProductCreate]):
    db = next(get_db())
    with db.begin():
        for item in products:
            product = Product(**item)
            db.add(product)
