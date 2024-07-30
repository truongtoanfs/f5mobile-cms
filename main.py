from fastapi import FastAPI
from routes import categories, subcategories, products, images
from databases.database import create_tables

app = FastAPI()

app.include_router(categories.router)
app.include_router(subcategories.router)
app.include_router(products.router)
app.include_router(images.router)

if __name__ == "main":
    create_tables()
