from collections import namedtuple

import jinja2
from attr import dataclass

User = namedtuple('User', ['username', 'age'])


@dataclass
class UserData:
    username: str | None
    age: int | None


def _base_generate_template(base_object, base_template_data: str) -> str:
    environment = jinja2.Environment()
    base_template = environment.from_string(base_template_data)
    return base_template.render(**{base_object.__class__.__name__.lower():base_object})

def generate_template(user, template_data: str) -> str:
    return _base_generate_template(
        user, template_data
    )


def test_generate_template():
    user = User(
        username="userTest",
        age=3
    )
    current_template = """
    <html>
    <head>
    <title>{{ user.username}} {{user.age}}<title>
    </head>
    </html>
""".strip()
    awaited_result = f"""
    <html>
    <head>
    <title>{user.username} {user.age}<title>
    </head>
    </html>
""".strip()
    template_str = generate_template(user, current_template)

    assert template_str == awaited_result, f"{template_str} != {awaited_result}"

def test_generate_template_incomplete_data():
    new_user = UserData(
        age=None,
        username="testUser"
    )
    current_template = """
        <html>
        <head>
        <title>{{ userdata.username }} {{
        userdata.age if userdata.age else "Не задан параметр возраста"
        }}<title>
        </head>
        </html>
    """.strip()

    awaited_result = f"""
        <html>
        <head>
        <title>{new_user.username} Не задан параметр возраста<title>
        </head>
        </html>
    """.strip()

    new_template = generate_template(new_user, current_template)

    assert new_template == awaited_result, f"{new_template} != {awaited_result}"