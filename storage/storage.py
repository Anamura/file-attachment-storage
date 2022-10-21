import hashlib
import os
import aiofiles
import asyncio
from aiohttp import web

from logger import get_default_logger

logger = get_default_logger('Store')
remote_path = 'store'


async def upload(file_data, chunk_size=32768):
    path = os.path.join(remote_path, file_data.name)
    m = hashlib.md5()

    async with aiofiles.open(path, "wb") as f:
        while True:
            buf = await file_data.read_chunk(chunk_size)
            if not buf:
                break
            m.update(buf)
            await f.write(buf)

    f_hash = m.hexdigest()
    print(f_hash)
    logger.debug('Uploaded files to store.')

    os.makedirs(os.path.join(remote_path, f_hash[:2]), exist_ok=True)
    os.replace(path, os.path.join(remote_path, f_hash[:2], f_hash))
    return f_hash


def delete_file(file_hash):
    if file_hash is None:
        raise ValueError("Hash value is empty, can't delete().")
    path = os.path.join(remote_path, file_hash[:2], file_hash)
    try:
        os.remove(path)

        dirname = os.path.dirname(path)
        if not os.listdir(dirname):
            os.rmdir(dirname)
    except FileNotFoundError:
        pass


async def download(file):
    path = os.path.join(remote_path, file[:2], file)
    if os.path.exists(path):
        async with aiofiles.open(path, 'rb') as f:
            return web.Response(headers={'Content-Type': 'multipart/form-data'},
                                body=await f.read())
    else:
        return web.json_response('no such file', status=404)
