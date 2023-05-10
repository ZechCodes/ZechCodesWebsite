from starlette.applications import Starlette, Request
from starlette.responses import RedirectResponse
from starlette.routing import Route
from typing import Awaitable, Callable

blog_site = "https://blog.zech.codes"


def get_blog_redirect_routes():
    redirect_blog_slugs = [
        "terrible-but-cool-code-metaclasses",
        "moving-on-from-discordpy",
        "try-except-else",
        "how-to-use-anyall-efficiently-in-python",
    ]
    return (
        Route(f"/{slug}", _create_redirect_handler(f"{blog_site}/{slug}", 301))
        for slug in redirect_blog_slugs
    )


def _create_redirect_handler(
    url: str, status_code: int = 302
) -> Callable[[Request], Awaitable[RedirectResponse]]:
    async def redirect(request: Request) -> RedirectResponse:
        return RedirectResponse(url, status_code)

    return redirect


app = Starlette(
    routes=[
        Route("/", _create_redirect_handler(blog_site), name="index"),
        Route(
            "/discord",
            _create_redirect_handler("https://discord.gg/de8kajxbYS"),
            name="discord-invite",
        ),
        Route(
            "/bevy",
            _create_redirect_handler("https://bevy.zech.codes/"),
            name="bevy-docs",
        ),
        Route(
            "/github",
            _create_redirect_handler("https://github.com/ZechCodes/"),
            name="github",
        ),
        *get_blog_redirect_routes(),
    ]
)
