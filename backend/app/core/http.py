import httpx

async_client: httpx.AsyncClient | None = None

async def get_async_client() -> httpx.AsyncClient:
    global async_client
    if async_client is None:
        async_client = httpx.AsyncClient(timeout=30.0)
    return async_client

async def shutdown_async_client() -> None:
    global async_client
    if async_client is not None:
        await async_client.aclose()
        async_client = None
