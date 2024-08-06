import os
from fastapi import APIRouter, UploadFile, Path, HTTPException, status
from fastapi.responses import FileResponse
from typing import Annotated
from models import SuccessStatus
from utils.common import check_file_existence

router = APIRouter(prefix="/api", tags=["Images"])


images_directory = os.path.join(os.getcwd(), "images")

@router.get("/images", response_model=list[str])
def list_images():
    file_names = os.listdir(images_directory)
    paths = []
    for name_file in file_names:
        file_path = f"/api/images/{name_file}"
        paths.append(file_path)
    return paths


@router.post("/images", response_model=SuccessStatus)
async def upload_images(files: list[UploadFile]):
    try:
        for file in files:
            if not file.content_type.startswith("image/"):
                raise ValueError("File must be an image")
            with open(f"images/{file.filename}", "wb") as file_open:
                data = await file.read()
                file_open.write(data)
        return SuccessStatus()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/images/{file_name}", response_class=FileResponse)
def detail_image(
    file_name: Annotated[str, Path(description="valid format: file_name.jpg")]
):
    image_path = check_file_existence(directory=images_directory, file_name=file_name)

    return FileResponse(image_path)


@router.delete("/images/{file_name}", response_model=SuccessStatus)
async def delete_image(
    file_name: Annotated[str, Path(description="valid format: file_name.jpg")]
):
    image_path = check_file_existence(directory=images_directory, file_name=file_name)
    os.remove(image_path)

    return SuccessStatus()
