from unittest.mock import patch

import pytest

from github_stars import api_get, get_github_stars


def test_api_get():
    with patch("requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = [{"repo": "test_repo"}]
        mocked_get.return_value.links = {"next": {"url": "next_url"}}

        results, next_page = api_get("some_url", {}, {})
        assert results == [{"repo": "test_repo"}]
        assert next_page == {"url": "next_url"}


def test_get_github_stars():
    with patch("github_stars.api_get") as mocked_api_get:
        mocked_api_get.side_effect = [
            ([{"repo": "test_repo"}], {"url": "next_url"}),
            ([{"repo": "test_repo2"}], None),
        ]

        starred_repos = get_github_stars("some_username")
        assert starred_repos == [{"repo": "test_repo"}, {"repo": "test_repo2"}]
