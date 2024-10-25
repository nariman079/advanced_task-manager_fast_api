from services import create_object, get_object_by_id, get_objects
import redis

test_db = redis.Redis(
    host="redis",
    port=6379,
    db=1
)

new_obj = create_object(
    {
        'id': 1,
        'username': "test"
    },
    test_db
)
objects = get_objects(test_db)

object_first = get_object_by_id(
    1, test_db
)

assert object_first == {
        'id': 1,
        'username': "test"
    }, f"Data error {object_first}"
assert new_obj ==  {
        'id': 1,
        'username': "test"
    }, f"Data error {new_obj}"

print("Successfull tests!")
test_db.flushdb()