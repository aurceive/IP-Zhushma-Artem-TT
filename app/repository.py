from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models import User
from app.schemas import UserCreate, UserUpdate

class UserRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def create_user(self, data: UserCreate) -> User:
    user = User(**data.model_dump())
    self.session.add(user)
    await self.session.commit()
    await self.session.refresh(user)
    return user

  async def list_users(self) -> list[User]:
    result = await self.session.execute(select(User))
    return list(result.scalars().all())

  async def get_user(self, user_id: int) -> User | None:
    result = await self.session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

  async def update_user(self, user_id: int, data: UserUpdate) -> User | None:
    user = await self.get_user(user_id)
    if not user:
      return None
    for key, value in data.model_dump(exclude_unset=True).items():
      setattr(user, key, value)
    await self.session.commit()
    await self.session.refresh(user)
    return user

  async def delete_user(self, user_id: int) -> bool:
    result = await self.session.execute(delete(User).where(User.id == user_id))
    await self.session.commit()
    return result.rowcount > 0
