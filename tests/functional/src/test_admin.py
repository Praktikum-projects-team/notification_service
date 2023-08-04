from http import HTTPStatus

import pytest

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
