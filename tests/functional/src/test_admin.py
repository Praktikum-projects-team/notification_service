from http import HTTPStatus

import pytest

from tests.functional.testdata.admin import get_notification_data
from tests.functional.utils.routes import ADMIN_URL

pytestmark = pytest.mark.asyncio


class TestFilm:
    async def test_get_notifications(self, make_get_request):

        response = await make_get_request(ADMIN_URL)

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert 'events' in response.body, f'No "events" in response'

        expected_fields = ('id', 'description', 'is_unsubscribeable', 'cron_string')
        for _ in response.body['events']:
            for field in expected_fields:
                assert field in response.body, f'No {field} in response'

    async def test_get_notification(self, make_get_request, make_post_request):
        data = get_notification_data()
        await make_post_request(ADMIN_URL, data=data)

        response = await make_get_request(f'{ADMIN_URL}/{data["id"]}')

        assert response.status == HTTPStatus.OK, 'Wrong status code'

    async def test_add_notification(self, make_post_request):
        data = get_notification_data()
        response = await make_post_request(ADMIN_URL, data=data)

        assert response.status == HTTPStatus.CREATED, 'Wrong status code'
        assert response.body['msg'] == 'Notification added', 'Wrong message'

    async def test_update_notification(self, make_put_request, make_post_request):
        data = get_notification_data()
        await make_post_request(ADMIN_URL, data=data)
        response = await make_put_request(f'{ADMIN_URL}/{data["id"]}', data=data)

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert response.body['msg'] == 'Notification updated', 'Wrong message'

    async def test_delete_notification(self, make_delete_request, make_post_request):
        data = get_notification_data()
        await make_post_request(ADMIN_URL, data=data)
        response = await make_delete_request(f'{ADMIN_URL}/{data["id"]}')

        assert response.status == HTTPStatus.NO_CONTENT, 'Wrong status code'
