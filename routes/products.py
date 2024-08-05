from fastapi import APIRouter, UploadFile, status, HTTPException, Query
import pandas as pd
import json
from typing import Annotated
from datetime import datetime


from models import (
    SuccessStatus,
    ProductCreate,
    ProductList,
    ProductPublic,
    ProductUpdate,
)
from utils.common import (
    get_db_products,
    get_product,
    update_db_product,
    get_category,
    get_subcategory,
)
from dependencies import SessionDepend

from workers.tasks import writeDb


router = APIRouter(prefix="/api", tags=["Products"])


def handleExel(excel_file):
    try:
        with pd.ExcelFile(excel_file) as xls:
            data = pd.read_excel(xls)
            products_json = data.to_json(orient="records")
            products_list = json.loads(products_json)
            products_data = []
            for item in products_list:
                product = ProductCreate(**item)
                products_data.append(product.model_dump())
            return products_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/products", response_model=ProductList)
def list_product(
    db: SessionDepend,
    name: str | None = None,
    limit: Annotated[int, Query(gt=0)] = 100,
    page: Annotated[int, Query(gt=0)] = 1,
    sort_key: Annotated[str, Query(pattern="^(new_price|created_at|name|old_price|updated_at)$")] = "name",
    order_by: Annotated[str, Query(pattern="^(desc|asc)$")] = "desc",
):
    db_products = get_db_products(db=db, name=name, limit=limit, page=page, order_by=order_by, sort_key=sort_key)
    return db_products


@router.post("/products", response_model=SuccessStatus)
def create_product(product: ProductCreate, db: SessionDepend):
    if product.category_id:
        _ = get_category(category_id=product.category_id, db=db)
    if product.subcategory_id:
         _ = get_subcategory(subcategory_id=product.subcategory_id, db=db)

    products = [product.model_dump()]
    writeDb(products=products)
    return SuccessStatus()


@router.post("/products/many", response_model=SuccessStatus)
def create_many_product(product_file: UploadFile):
    if not product_file.filename.lower().endswith((".xls", ".xlsx")):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only support format .xls and xlsx",
        )
    products = handleExel(product_file.file)
    writeDb(products=products)
    return SuccessStatus()


@router.get("/products/{product_id}", response_model=ProductPublic)
def get_product_detail(db: SessionDepend, product_id: str):
    db_product = get_product(product_id=product_id, db=db)
    return db_product


@router.patch("/products/{product_id}", response_model=ProductPublic)
def update_product(product_id: str, product: ProductUpdate, db: SessionDepend):
    db_product = get_product(product_id=product_id, db=db)
    payload = product.model_dump(exclude_unset=True)
    payload["updated_at"] = datetime.now()
    update_db_product(db, product_id, payload)
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", response_model=SuccessStatus)
def delete_product(product_id: str, db: SessionDepend):
    db_product = get_product(product_id=product_id, db=db)
    db.delete(db_product)
    db.commit()
    return SuccessStatus()
