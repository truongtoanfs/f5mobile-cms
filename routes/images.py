import os
from fastapi import APIRouter, UploadFile, Path, HTTPException, status
from typing import Annotated
from models import SuccessStatus

router = APIRouter(prefix="/api", tags=["Images"])


images_directory = os.path.join(os.getcwd(), "images")


@router.get("/images", response_model=list[str])
def list_images():
    file_names = os.listdir(images_directory)
    paths = []
    for name_file in file_names:
        file_path = os.path.join(images_directory, name_file)
        paths.append(file_path)
    return paths


@router.post("/images", response_model=list[str])
async def upload_images(files: list[UploadFile]):
    try:
        saved_file_paths = []

        for file in files:
            file_path = os.path.join(images_directory, file.filename)
            with open(f"images/{file.filename}", "wb") as file_open:
                data = await file.read()
                file_open.write(data)
            saved_file_paths.append(file_path)
        return saved_file_paths
    except Exception as e:
        print(f"Error: {str(e)}")


@router.delete("/images/{file_name}", response_model=SuccessStatus)
async def delete_image(
    file_name: Annotated[str, Path(description="valid format: file_name.jpg")]
):
    print(type(file_name))
    file_names = os.listdir(images_directory)
    if file_names.count(file_name) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="file not exit!"
        )
    os.remove(f"images/{file_name}")
    return SuccessStatus()
