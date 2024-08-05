from fastapi import APIRouter
from sqlmodel import select, update, func, col
from models import (
    SubcategoryList,
    Subcategory,
    SubcategoryPublic,
    SubcategoryCreate,
    SubcategoryDetail,
    SubcategoryUpdate,
    SuccessStatus,
)
from utils.common import get_subcategory, get_category
from dependencies import SessionDepend


router = APIRouter(prefix="/api", tags=["Subcategories"])


@router.get("/subcategories", response_model=SubcategoryList)
def list_subcategory(db: SessionDepend):
    db_subcategories = db.exec(select(Subcategory)).all()
    total = db.exec(select(func.count(col(Subcategory.id)))).one()
    return SubcategoryList(data=db_subcategories, total=total)


@router.post("/subcategories", response_model=SubcategoryPublic)
def create_subcategory(subcategory: SubcategoryCreate, db: SessionDepend):
    _ = get_category(category_id=subcategory.category_id, db=db)

    subcategory_data = subcategory.model_dump()
    db_subcategory = Subcategory(**subcategory_data)
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


@router.get("/subcategories/{subcategory_id}", response_model=SubcategoryDetail)
def get_subcategory_detail(db: SessionDepend, subcategory_id: str):
    db_database = get_subcategory(subcategory_id=subcategory_id, db=db)
    return db_database


@router.patch("/subcategories/{subcategory_id}")
def update_subcategory(
    subcategory_id: str, subcategory: SubcategoryUpdate, db: SessionDepend
):
    db_subcategory = get_subcategory(subcategory_id=subcategory_id, db=db)
    payload = subcategory.model_dump(exclude_unset=True)
    statement = (
        update(Subcategory).where(Subcategory.id == subcategory_id).values(**payload)
    )
    db.exec(statement)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


@router.delete("/subcategories/{subcategory_id}", response_model=SuccessStatus)
def delete_subcategory(subcategory_id: str, db: SessionDepend):
    db_subcategory = get_subcategory(subcategory_id, db)
    db.delete(db_subcategory)
    db.commit()
    return SuccessStatus()
