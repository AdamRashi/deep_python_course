import time
import json
import ujson
import cjson
from faker import Faker


N_OBJECTS = 30000

fake = Faker()
print('------------------------------------------')
print('Generating JSON data for benchmark test...')
# Генерация большого количества случайных JSON-объектов
data = []
for _ in range(N_OBJECTS):
    obj = {
        'name': fake.name(),
        'address': fake.address(),
        'phone_number': fake.phone_number(),
        'email': fake.email()
    }
    data.append(obj)

# Измерение времени выполнения для модуля json
start_time = time.time()
json_res = [json.dumps(dct) for dct in data]
json_time = time.time() - start_time

print("время выполнения json.dumps: ", json_time)

# Измерение времени выполнения для модуля ujson
start_time = time.time()
ujson_res = [ujson.dumps(dct) for dct in data]
ujson_time = time.time() - start_time

print("время выполнения ujson.dumps: ", ujson_time)

# Измерение времени выполнения для модуля cjson
start_time = time.time()
cjson_res = [cjson.dumps(dct) for dct in data]
cjson_time = time.time() - start_time

print("время выполнения cjson.dumps: ", cjson_time)
