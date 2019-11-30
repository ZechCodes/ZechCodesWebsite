from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route


async def homepage(request):
    return HTMLResponse("<h1>Hello World</h1>", status_code=200)


routes = [Route("/", endpoint=homepage)]

app = Starlette(debug=True, routes=routes)
