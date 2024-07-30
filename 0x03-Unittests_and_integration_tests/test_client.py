#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock, call
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch('client.get_json')
    def test_org(
                 self, org_name: str,
                 expected_response: Dict,
                 mock_get_json: MagicMock
                ) -> None:
        """
        Test org method of GithubOrgClient class.

        Args:
            org_name (str): The name of the organization.
            expected_response (Dict): The expected response data.
            mock_get_json (MagicMock): Mock object for get_json function.
        """

        mock_get_json.return_value = MagicMock(return_value=expected_response)
        github_org_client = GithubOrgClient(org_name)
        self.assertEqual(github_org_client.org(), expected_response)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org_name)
        )

    def test_public_repos_url(self) -> None:
        """
        Tests the `_public_repos_url` property.
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            public_repos = "https://api.github.com/users/google/repos"
            mock_org.return_value = {
                'repos_url': public_repos,
            }

            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                public_repos,
            )

    @patch('client.get_json')
    def test_public_repos(self, mocked_get_json):
        """
        Test public_repos method.
        """
        payload = [{"name": "Google"}, {"name": "TT"}]
        mocked_get_json.return_value = payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mocked_public_repos_url:
            mocked_public_repos_url.return_value = "world"

            response = GithubOrgClient('test').public_repos()

            self.assertEqual(response, ["Google", "TT"])

            mocked_public_repos_url.assert_called_once()
            mocked_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, key, expectation):
        """
        Test has_license method.
        """
        result = GithubOrgClient.has_license(repo, key)
        self.assertEqual(result, expectation)


@parameterized_class(['org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'], TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient.public_repos method.
    """

    @classmethod
    def setUpClass(cls):
        # Patch requests.get
        cls.get_patcher = patch('client.requests.get')
        cls.mocked_get = cls.get_patcher.start()
        # Set side effects for the mock
        cls.mocked_get.side_effect = [
            cls._mock_response(cls.org_payload),
            cls._mock_response(cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    @staticmethod
    def _mock_response(json_data, status=200):
        """
        Helper method to create a mock response object with the specified JSON data.
        """
        mock_resp = unittest.mock.Mock()
        mock_resp.json.return_value = json_data
        mock_resp.status_code = status
        return mock_resp

    def test_public_repos(self):
        """
        Test the public_repos method of the GithubOrgClient class.
        """
        # Create an instance of GithubOrgClient
        google_client = GithubOrgClient('Google')

        # Check if the org method returns the correct org_payload
        self.assertEqual(google_client.org, self.org_payload)

        # Check if the public_repos method returns the correct repos_payload
        self.assertEqual(google_client.public_repos(), self.expected_repos)
        self.assertEqual(google_client.public_repos("NONEXISTENT"), [])

        # Check if the correct URLs were called
        self.mocked_get.assert_has_calls([
            call("https://api.github.com/orgs/Google"),
            call(self.org_payload["repos_url"])
        ])


    def test_public_repos_with_license(self) -> None:
        """
        Test public_repos method of the GithubOrgClient class
        with a specified license.

        Verifies that the public_repos method returns the expected list
        of repositories associated with a GitHub organization
        that have a specific license.

        Returns:
            None
        """
        google_client = GithubOrgClient('Google')

        url = "https://api.github.com/orgs/Google"
        self.mocked_get.side_effect = [self.org_payload, self.repos_payload]

        self.assertEqual(google_client.org, self.org_payload)
        self.assertEqual(google_client.repos_payload, self.repos_payload)
        self.assertEqual(google_client.public_repos(), self.expected_repos)
        self.assertEqual(google_client.public_repos("NONEXISTENT"), [])
        self.assertEqual(google_client.public_repos("apache-2.0"),
                         self.apache2_repos)
        self.mocked_get.assert_has_calls([
            call(url),
            call(self.org_payload["repos_url"])
        ])

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up after the integration tests.

        Stops the patcher used to mock requests.get
        during the integration tests.

        Returns:
            None
        """
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()
