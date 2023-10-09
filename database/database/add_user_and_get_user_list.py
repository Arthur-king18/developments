from database.database import session, Transactional
from database.database.models import User, Referral

from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy import or_, select, and_


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self):
        ...

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def get_user_list(
            self,
            limit: int = 12,
            prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


    @Transactional()
    async def create_user(
            self, email: str, password1: str, password2: str, username: str, full_name: str
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException # Вывод ошибки типа
            # class PasswordDoesNotMatchException(CustomException):
            #    code = 401
            #    error_code = "USER__PASSWORD_DOES_NOT_MATCH"
            #   message = "password does not match"

        query = select(User).where(User.email == email)
        result = await session.execute(query)
        is_email_exist = result.scalars().first()

        if is_email_exist:
            raise DuplicateEmailException

        query = select(User).where(User.username == username)
        result = await session.execute(query)
        is_username_exist = result.scalars().first()

        if is_username_exist:
            raise DuplicateUsernameException

        user = User(email=email, password=pwd_context.hash(password1), username=username, full_name=full_name,
                    credits=0)

        user.referral.append(Referral()) # Подставляется целая моделька
        session.add(user)


    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

