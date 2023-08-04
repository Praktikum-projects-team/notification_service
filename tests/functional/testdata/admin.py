import uuid
from faker import Faker


fake = Faker()


async def get_notification_data() -> dict:
    data = {
        'id': str(uuid.uuid4()),
        'description': fake.text(max_nb_chars=200),
        'is_unsubscribeable': True,
        'cron_string': '0 0 * * * *',
    }

    return data
