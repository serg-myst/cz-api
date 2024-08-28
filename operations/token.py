from sqlalchemy import select
from operations.models import Token
from sqlalchemy.exc import SQLAlchemyError
from operations.database import async_session_maker
from logger import log


async def get_token():
    async with async_session_maker() as session:
        try:
            query = select(Token).where(Token.token_type == 'CZ')
            result = await session.scalars(query)
            res = result.first()
            log.info("get jwt token")
            return res.jwt_token
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            log.error(f"get token error {e}")
            raise RuntimeError(error) from e
        finally:
            await session.close()
