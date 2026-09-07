from pathlib import Path

import aiofiles
from fastapi import UploadFile

UPLOAD_DIR = Path("app/uploads")
CHUNK_SIZE = 8 * 1024 * 1024


async def save_upload_file(file: UploadFile) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = Path(file.filename or "upload").name
    destination = UPLOAD_DIR / filename

    async with aiofiles.open(destination, "wb") as out_file:
        while True:
            chunk = await file.read(CHUNK_SIZE)

            if not chunk:
                break

            await out_file.write(chunk)

    await file.close()

    return destination
