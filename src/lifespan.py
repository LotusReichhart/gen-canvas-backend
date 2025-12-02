from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select, func
from loguru import logger

from src.core.data.database.model.banner_entity import BannerEntity


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup...")

    try:
        db_wrapper = app.container.database_package.db()
        redis_client = app.container.external_service_package.redis_client()
    except AttributeError as e:
        logger.error(f"❌ Container Wiring Error: {e}. Kiểm tra lại tên package trong containers.py")
        raise e

    try:
        logger.info("Initializing Database (Extensions & Tables)...")
        await db_wrapper.create_database()
        logger.info("Database initialized.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    try:
        async with db_wrapper.session() as session:
            banner_count = await session.scalar(select(func.count(BannerEntity.id)))

            if banner_count == 0:
                logger.info("No banners found. Seeding default banners...")
                default_banners = [
                    BannerEntity(
                        title="Sáng Tạo Không Giới Hạn",
                        image_url="https://gen-canvas-s3-bucket.s3.ap-southeast-2.amazonaws.com/images/banners/banner_03.png",
                        display_order=1,
                        is_active=True
                    ),
                    BannerEntity(
                        title="Khám Phá Prompt Tuyệt Đỉnh",
                        image_url="https://gen-canvas-s3-bucket.s3.ap-southeast-2.amazonaws.com/images/banners/banner_02.png",
                        display_order=2,
                        is_active=True
                    ),
                    BannerEntity(
                        title="Biến Câu Từ thành Tuyệt Tác",
                        image_url="https://gen-canvas-s3-bucket.s3.ap-southeast-2.amazonaws.com/images/banners/banner_01.png",
                        display_order=3,
                        is_active=True
                    )
                ]
                session.add_all(default_banners)
                await session.commit()
                logger.info("Default banners seeded successfully.")
            else:
                logger.info(f"Found {banner_count} banners. Skipping seed.")
    except Exception as e:
        logger.error(f"Seeding data failed: {e}")

    try:
        await redis_client.ping()
    except Exception as e:
        logger.error(f"Redis connection check failed: {e}")

    yield

    logger.info("Application shutdown...")