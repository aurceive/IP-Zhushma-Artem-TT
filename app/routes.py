import subprocess
from litestar import Controller, Response, get, post, patch, delete
from litestar.di import Provide
from litestar.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserRead, UserUpdate
from app.repository import UserRepository
from app.config import get_session


class MainController(Controller):
  path = "/"
  dependencies = {"session": Provide(get_session)}

  @get("/")
  async def index(self) -> Response:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Main Page</title>
    </head>
    <body style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <h1>Main Page</h1>
      <div style="display: flex; gap: 10px; justify-content: center;">
        <form action="/apply-migration" method="post">
          <button type="submit">Apply migration</button>
        </form>
        <a href="/schema/swagger" target="_blank">
          <button type="button">Swagger</button>
        </a>
      </div>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")
    
  
  @post("/apply-migration")
  async def apply_migration(self) -> Response:
    try:
      # Run the Alembic command to apply migrations
      result = subprocess.run(["alembic", "upgrade", "head"], check=True, capture_output=True, text=True)
      html_content = f"""
      <!DOCTYPE html>
      <html>
      <head>
        <title>Migration Result</title>
      </head>
      <body style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <h1>Migration applied successfully</h1>
        <pre>{result.stdout}</pre>
        <a href="/"><button type="button">Back to Main Page</button></a>
      </body>
      </html>
      """
      return Response(content=html_content, media_type="text/html")
    except subprocess.CalledProcessError as e:
      html_content = f"""
      <!DOCTYPE html>
      <html>
      <head>
        <title>Migration Error</title>
      </head>
      <body style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <h1>Migration Error</h1>
        <pre>{e.stderr}</pre>
        <a href="/"><button type="button">Back to Main Page</button></a>
      </body>
      </html>
      """
      return Response(content=html_content, media_type="text/html")


class UserController(Controller):
  path = "/users"
  dependencies = {"session": Provide(get_session)}

  @post("/")
  async def create_user(self, data: UserCreate, session: AsyncSession) -> UserRead:
    repo = UserRepository(session)
    user = await repo.create_user(data)
    return UserRead.model_validate(user)

  @get("/")
  async def list_users(self, session: AsyncSession) -> list[UserRead]:
    repo = UserRepository(session)
    users = await repo.list_users()
    return [UserRead.model_validate(u) for u in users]

  @get("/{user_id:int}")
  async def get_user(self, user_id: int, session: AsyncSession) -> UserRead:
    repo = UserRepository(session)
    user = await repo.get_user(user_id)
    if not user:
      raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

  @patch("/{user_id:int}")
  async def update_user(self, user_id: int, data: UserUpdate, session: AsyncSession) -> UserRead:
    repo = UserRepository(session)
    user = await repo.update_user(user_id, data)
    if not user:
      raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

  @delete("/{user_id:int}")
  async def delete_user(self, user_id: int, session: AsyncSession) -> None:
    repo = UserRepository(session)
    success = await repo.delete_user(user_id)
    if not success:
      raise HTTPException(status_code=404, detail="User not found")
    return None