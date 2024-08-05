from fastapi import HTTPException, status
from models import ProductCreate, Product
from celery_config import app
from dependencies import get_db


@app.task
def writeDb(products: list[ProductCreate]):
    db = next(get_db())
    try:
        with db.begin():
            for item in products:
                product = Product(**item)
                db.add(product)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

