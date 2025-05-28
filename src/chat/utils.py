from fastapi import UploadFile

async def upload_photo(file: UploadFile):
    content = await file.read()
    with open(f"./{file.filename}", "wb") as f:
        f.write(content);
    return