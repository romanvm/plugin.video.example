# License: GPL v3: http://www.gnu.org/copyleft/gpl.html
# This is a very minimalistic example of unit testing for Kodi addons.
# Perquisites:
# xbmcstubs: https://github.com/romanvm/xbmcstubs
# mock: https://pypi.python.org/pypi/mock
__author__ = 'Roman_V_M'

import unittest
import os
import sys
import mock
# Add our plugin to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugin.video.expample'))
# Mock plugin call parameters so that our plugin can be imported correctly
with mock.patch('sys.argv', ['plugin://plugin.video.example', '5', '']):
    # Import our plugin for testing
    import default


class RouterTestCase(unittest.TestCase):
    """
    Test router function

    router() function includes custom logic for calling other
    functions depending on a provided paramstring.
    So it's a good candidate for unit testing.
    We don't test other functions here
    so they are replaced with mocks.
    """
    @mock.patch('default.list_categories')
    def test_router_with_no_params(self, mock_list_categories):
        """
        Test router with an empty paramstring
        """
        default.router('')
        mock_list_categories.assert_called_with()

    @mock.patch('default.list_videos')
    def test_router_list_videos(self, mock_list_videos):
        """
        Test router for open a category request
        """
        default.router('action=listing&category=Animals')
        mock_list_videos.assert_called_with('Animals')

    @mock.patch('default.play_video')
    def test_router_play_video(self, mock_play_video):
        """
        Test router for a play video request
        """
        default.router('action=play&video=http://test')
        mock_play_video.assert_called_with('http://test')

# list_categories(), list_videos() and play_video() functions include
# mostly calls to Kody Python API with little or no custom logic.
# So they are bad candidates for unit testing outside Kodi.
# They are better tested on a running Kodi instance.
# It is always a good idea to separate Kodi and non-Kodi logic
# into separate units of code (functions, classes, modules).

if __name__ == '__main__':
    # Run our tests
    unittest.main()
