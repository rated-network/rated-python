import os
from unittest import mock

import rated


def test_can_provision_api_key_from_environment():
    with mock.patch.dict(os.environ, {"RATED_API_KEY": "ey...0x69"}):
        r = rated.Rated()

        assert r.api_key == os.environ["RATED_API_KEY"]


def test_manually_setting_api_key_overrides_environment():
    with mock.patch.dict(os.environ, {"RATED_API_KEY": "ey...0x69"}):
        r = rated.Rated("ey...MyKey")

        assert r.api_key != os.environ["RATED_API_KEY"]
        assert r.api_key == "ey...MyKey"
