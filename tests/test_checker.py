import pytest, respx, httpx
from app.checker import check_site
from app.models import Site

@pytest.mark.asyncio
@respx.mock
async def test_check_site_up():
    respx.get("https://example.com").mock(return_value=httpx.Response(200))
    site = Site(id=1, name="x", url="[example.com](https://example.com)", is_active=True)
    log = await check_site(site)
    assert log.is_up and log.status_code == 200
