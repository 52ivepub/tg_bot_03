

import asyncpg


pool_connect = asyncpg.create_pool(user='postgres', password='1', database='bot', 
                                             host='127.0.0.1', port=5432, command_timeout=60)

