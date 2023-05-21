import asyncio
import sys
import aiohttp

responses = {}

async def main():
    domain_list = sys.argv[1]
    async with aiohttp.ClientSession() as session:
        for port in range(1, 65536):
            with open(domain_list) as f:
                for line in f:
                    url = 'https://{}:{}'.format(line.strip(), port)
                    try:
                        async with session.get(url, timeout=0.3) as response:
                            if response.status == 200:
                                print(response)
                                if response.status not in responses:
                                    responses[response.status] = []
                                responses[response.status].append(port)
                    except (aiohttp.client_exceptions.ClientConnectorError, asyncio.exceptions.TimeoutError,aiohttp.client_exceptions.ClientResponseError):
                        pass

asyncio.run(main())
for status, ports in responses.items():
    print('Ports {} responded with status {}'.format(ports, status))
