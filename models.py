from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime


class CategoryBase(SQLModel):
    name: str = Field(unique=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryPublic(CategoryBase):
    id: str = Field(primary_key=True, default_factory=uuid.uuid4)


class Category(CategoryPublic, table=True):
    subcategories: list["Subcategory"] = Relationship(back_populates="category")
    products: list["Product"] = Relationship(back_populates="category")


class CategoryList(SQLModel):
    data: list[CategoryPublic]
    total: int


class CategoryDetail(CategoryPublic):
    subcategories: list["Subcategory"] = []
    products: list["Product"] = []


# -- Subcategory --
class SubcategoryBase(SQLModel):
    category_id: str = Field(foreign_key=("category.id"))
    name: str = Field(unique=True)


class SubcategoryCreate(SubcategoryBase):
    pass


class SubcategoryPublic(SubcategoryBase):
    id: str = Field(primary_key=True, default_factory=uuid.uuid4)


class Subcategory(SubcategoryPublic, table=True):
    category: Category = Relationship(back_populates="subcategories")
    products: list["Product"] = Relationship(back_populates="subcategory")


class SubcategoryList(SQLModel):
    data: list[SubcategoryPublic]
    total: int


class SubcategoryDetail(SubcategoryPublic):
    products: list["Product"] = []


class SubcategoryUpdate(SQLModel):
    category_id: str | None = None
    name: str | None = None


# -- Product --
class ProductBase(SQLModel):
    name: str = Field(unique=True)
    category_id: str = Field(foreign_key=("category.id"))
    subcategory_id: str | None = Field(default=None, foreign_key=("subcategory.id"))
    old_price: int | None = None
    new_price: int
    avatar_url: str
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductPublic(ProductBase):
    id: str = Field(primary_key=True, default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None


class Product(ProductPublic, table=True):
    category: Category = Relationship(back_populates="products")
    subcategory: Subcategory = Relationship(back_populates="products")


class ProductList(SQLModel):
    data: list[ProductPublic] = []
    total: int


class ProductUpdate(ProductBase):
    name: str | None = None
    category_id: str | None = None
    new_price: int | None = None
    avatar_url: str | None = None


# -- Common --
class SuccessStatus(SQLModel):
    status: str = "Success"
