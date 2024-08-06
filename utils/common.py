import os
from sqlmodel import select, Session, update, func, desc, asc
from models import Category, Subcategory, Product
from fastapi import HTTPException, status


def get_category(category_id: str, db: Session):
    db_category = db.get(Category, category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!"
        )
    return db_category


def get_subcategory(subcategory_id: str, db: Session):
    db_subcategory = db.get(Subcategory, subcategory_id)
    if db_subcategory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found!"
        )
    return db_subcategory


def get_db_products(
    db: Session,
    limit: int,
    page: int,
    sort_key: str,
    order_by: str,
    name: str | None = None
):
    offset = (page - 1) * limit

    if name is None:
        query = select(Product)
    else:
        search_name = "%{}%".format(name)
        query = select(Product).filter(Product.name.like(search_name))
    
    sort_column = getattr(Product, sort_key)
    if (order_by ==  "asc"):
        data = db.exec(query.limit(limit).offset(offset).order_by(asc(sort_column))).all()
    else:
        data = db.exec(query.limit(limit).offset(offset).order_by(desc(sort_column))).all()

    count_query = select(func.count()).select_from(query.subquery())
    total = db.exec(count_query).one()
    return {"data": data, "total": total}


def get_product(db: Session, product_id: str):
    db_product = db.get(Product, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!"
        )
    return db_product


def update_db_product(db: Session, product_id: str, payload: dict):
    try:
        statement = update(Product).where(Product.id == product_id).values(**payload)
        db.exec(statement)
        db.commit()
    except Exception as e:
        print("The error is: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error update database!",
        )
    
def check_file_existence(directory: str, file_name: str):
    file_names = os.listdir(directory)
    if file_names.count(file_name) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="file not exit!"
        )
    return os.path.join(directory, file_name)
