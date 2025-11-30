from aiobotocore.session import get_session
from loguru import logger

async def init_s3_client(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    region_name: str
):
    session = get_session()
    async with session.create_client(
        's3',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    ) as client:
        logger.info("S3 Client Initialized")
        yield client
        logger.info("S3 Client Closed")