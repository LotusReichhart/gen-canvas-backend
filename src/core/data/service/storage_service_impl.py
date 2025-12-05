import os
from loguru import logger
from typing import List

import uuid

from fastapi import UploadFile
from aiobotocore.client import AioBaseClient

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException
from src.core.domain.service.storage_service import StorageService


class StorageServiceImpl(StorageService):
    def __init__(
            self,
            client: AioBaseClient,
            bucket_name: str,
            region: str):
        self._client = client
        self._bucket_name = bucket_name
        self._region = region
        self._base_url = f"https://{self._bucket_name}.s3.{self._region}.amazonaws.com"
        self._max_size = 5 * 1024 * 1024

    @staticmethod
    def _generate_file_name(original_filename: str) -> str:
        parts = original_filename.split(".")
        extension = parts[-1] if len(parts) > 1 else ""
        if extension:
            return f"{uuid.uuid4()}.{extension}"
        return str(uuid.uuid4())

    async def upload_file(self, file: UploadFile, destination_path: str) -> str:
        if not file or not file.filename:
            raise BusinessException(MsgKey.FILE_EMPTY, 400)

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0, os.SEEK_SET)

        if file_size == 0:
            raise BusinessException(MsgKey.FILE_EMPTY, 400)

        if file_size > self._max_size:
            raise BusinessException(MsgKey.FILE_TOO_LARGE, 413)

        file_name = self._generate_file_name(file.filename)

        destination_path = destination_path.strip("/")
        file_key = f"{destination_path}/{file_name}"

        try:
            file_content = await file.read()

            await self._client.put_object(
                Bucket=self._bucket_name,
                Key=file_key,
                Body=file_content,
                ContentType=file.content_type or "application/octet-stream"
            )

            image_url = f"{self._base_url}/{file_key}"

            logger.info(f"S3 Upload Success: {image_url}")

            return image_url
        except Exception as e:
            logger.error(f"S3 Upload Error: {e}")
            raise BusinessException(MsgKey.UPLOAD_FAILED, 500)

    async def delete_file(self, file_url: str) -> bool:
        if not file_url:
            return False

        if not file_url.startswith(self._base_url):
            logger.warning(f"Ignored delete request for external URL: {file_url}")
            return False

        file_key = file_url.replace(f"{self._base_url}/", "")

        if not file_key:
            return False

        try:
            await self._client.delete_object(
                Bucket=self._bucket_name,
                Key=file_key
            )
            logger.info(f"Deleted S3 Object: {file_key}")
            return True
        except Exception as e:
            logger.error(f"S3 Delete Error: {e}")
            return False

    async def get_files_in_path(self, path: str) -> List[str]:
        if not path:
            return []

        if not path.endswith('/'):
            path += '/'

        urls = []
        try:
            response = await self._client.list_objects_v2(
                Bucket=self._bucket_name,
                Prefix=path
            )

            for file_obj in response.get('Contents', []):
                file_key = file_obj.get('Key')
                if file_key and not file_key.endswith('/'):
                    urls.append(f"{self._base_url}/{file_key}")

            return urls

        except Exception as e:
            logger.error(f"S3StorageService get_files_in_path error: {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
