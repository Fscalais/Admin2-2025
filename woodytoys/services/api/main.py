import os, hashlib
import uuid
from datetime import datetime

from flask import Flask, request, make_response
from flask_cors import CORS

import woody
import redis

app = Flask('my_api')
cors = CORS(app)

# redis_db = redis.Redis(host='redis', port=6379, db=0)

# --- Redis & cache settings ---
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
CACHE_TTL = int(os.getenv('CACHE_TTL', '60'))
ENABLE_CACHE = os.getenv('ENABLE_CACHE', '1') == '1'
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

def _respond(body: str, cache_status: str):
    resp = make_response(body)
    resp.headers['X-Cache'] = cache_status  # HIT / MISS / BYPASS
    return resp

def _cache_key(prefix: str):
    raw = f"{prefix}:{request.path}?{request.query_string.decode()}"
    return hashlib.sha1(raw.encode()).hexdigest()

def _cached(prefix: str, producer, key: str | None = None):
    if not ENABLE_CACHE:
        return _respond(producer(), 'BYPASS')
    k = key or _cache_key(prefix)  # <-- permet d'imposer une clé fixe
    val = r.get(k)
    if val is not None:
        return _respond(val, 'HIT')
    val = producer()
    r.setex(k, CACHE_TTL, val)
    return _respond(val, 'MISS')

@app.get('/api/ping')
def ping():
    return 'ping'


# ### 1. Misc service ### (note: la traduction de miscellaneous est 'divers'
@app.route('/api/misc/time', methods=['GET'])
def get_time():
    return f'misc: {datetime.now()}'


@app.route('/api/misc/heavy', methods=['GET'])
def get_heavy():
    name = request.args.get('name')
    return _cached('heavy', lambda: f'{datetime.now()}: {woody.make_some_heavy_computation(name)}')


# ### 2. Product Service ###
@app.route('/api/products', methods=['GET'])
def add_product():
    product = request.args.get('product')
    woody.add_product(str(product))
    # Invalidation du cache "last"
    try:
        r.delete(_cache_key('last_product'))
    except Exception:
        pass
    return str(product) or "none"

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return "not yet implemented"


@app.route('/api/products/last', methods=['GET'])
def get_last_product():
    # clé fixe = "last_product"
    return _cached('last_product',
                   lambda: f'db: {datetime.now()} - {woody.get_last_product()}',
                   key='last_product')

# ### 3. Order Service
@app.route('/api/orders/do', methods=['GET'])
def create_order():
    # very slow process because some payment validation is slow (maybe make it asynchronous ?)
    # order = request.get_json()
    product = request.args.get('order')
    order_id = str(uuid.uuid4())

    # TODO TP10: this next line is long, intensive and can be done asynchronously ... maybe use a message broker ?
    process_order(order_id, product)

    return f"Your process {order_id} has been created with this product : {product}"


@app.route('/api/orders/', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id')
    status = woody.get_order(order_id)

    return f'order "{order_id}": {status}'


# #### 4. internal Services
def process_order(order_id, order):
    # ...
    # ... do many check and stuff
    status = woody.make_heavy_validation(order)

    woody.save_order(order_id, status, order)


if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
