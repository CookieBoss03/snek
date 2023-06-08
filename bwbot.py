#!/usr/bin/env python3

import asyncio
import secrets  # username, password


async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')


if __name__ == "__main__":
    asyncio.run(main())
