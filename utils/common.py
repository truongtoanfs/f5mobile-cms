from sqlmodel import select, Session, update, func, col
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
    name: str | None = None,
    limit: int | None = None,
    page: int | None = None,
):
    if limit is None:
        limit = 100
    if page is None:
        page = 1

    offset = (page - 1) * limit

    if name is not None:
        search_name = "%{}%".format(name)
        query = select(Product).filter(Product.name.like(search_name))
    else:
        query = select(Product)

    data = db.exec(query.limit(limit).offset(offset)).all()
    total = db.exec(select(func.count(col(Product.id)))).one()

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
