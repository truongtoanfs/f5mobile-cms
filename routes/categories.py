from fastapi import APIRouter
from sqlmodel import select, func, col

from models import (
    CategoryList,
    Category,
    CategoryCreate,
    CategoryUpdate,
    CategoryPublic,
    CategoryDetail,
    SuccessStatus,
)
from utils.common import get_category
from dependencies import SessionDepend


router = APIRouter(prefix="/api", tags=["Categories"])


@router.get("/categories", response_model=CategoryList)
def list_category(db: SessionDepend):
    db_categories = db.exec(select(Category)).all()
    total = db.exec(select(func.count(col(Category.id)))).one()
    print("total", type(total))
    return CategoryList(data=db_categories, total=total)


@router.post("/categories", response_model=CategoryPublic)
def create_category(category: CategoryCreate, db: SessionDepend):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories/{category_id}", response_model=CategoryDetail)
def get_category_detail(db: SessionDepend, category_id: str):
    db_category = get_category(category_id=category_id, db=db)
    return db_category


@router.put("/categories/{category_id}", response_model=CategoryPublic)
def update_category(category_id: str, category: CategoryUpdate, db: SessionDepend):
    db_category = get_category(category_id=category_id, db=db)
    db_category.name = category.name
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/categories/{category_id}", response_model=SuccessStatus)
def delete_categories(category_id: str, db: SessionDepend):
    db_category = get_category(category_id, db)
    db.delete(db_category)
    db.commit()
    return SuccessStatus()
