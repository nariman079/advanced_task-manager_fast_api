from aiohttp import ClientSession, ClientResponse


class Client:
    @staticmethod
    async def post(*args, **kwargs) -> tuple:
        async with ClientSession() as session:
            async with session.post(*args, **kwargs) as response:
                return await response.json(), response

    @staticmethod
    async def get(*args, **kwargs) -> tuple:
        async with ClientSession() as session:
            async with session.post(*args, **kwargs) as response:
                return await response.json(), response