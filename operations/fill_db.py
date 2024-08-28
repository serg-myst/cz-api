from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
import asyncio
from models import KizStatus, ProductGroup, PackageType, EmissionType, ReportStatus
from fill_db_config import KIZ_STATUS, PRODUCT_GROUP, PACKAGE_TYPE, EMISSION_TYPE, REPORT_STATUS
from database import async_session_maker


async def fill_table(table, file, pk):
    async with async_session_maker() as session:
        try:
            stmt = insert(table).values(file)
            do_update_stmt = stmt.on_conflict_do_nothing(index_elements=pk)
            await session.execute(do_update_stmt)
            await session.commit()
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()


if __name__ == '__main__':
    ...
    # asyncio.run(fill_table(KizStatus, KIZ_STATUS, ['Id']))
    # asyncio.run(fill_table(ProductGroup, PRODUCT_GROUP, ['Id']))
    # asyncio.run(fill_table(PackageType, PACKAGE_TYPE, ['Id']))
    # asyncio.run(fill_table(EmissionType, EMISSION_TYPE, ['Id']))
    # asyncio.run(fill_table(ReportStatus, REPORT_STATUS, ['Id']))
