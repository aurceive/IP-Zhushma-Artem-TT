from litestar import Litestar
from app.routes import MainController, UserController
from app.config import alchemy
from dotenv import load_dotenv
import os

load_dotenv()

debug = os.getenv("DEBUG", "false").lower() == "true"

app = Litestar(
  route_handlers=[MainController, UserController],
  plugins=[alchemy],
  debug=debug,
)

def run():
  import uvicorn
  uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)