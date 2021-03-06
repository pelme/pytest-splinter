"""Browser screenshot tests."""
import pytest

import mock

from _pytest.config import Config


def test_browser_screenshot_normal(testdir):
    """Test making screenshots on test failure.

    Normal test run.
    """
    testdir.inline_runsource("""
        def test_screenshot(browser):
            assert False
    """, "-vl", "--splinter-session-scoped-browser=false")

    assert testdir.tmpdir.join('test_browser_screenshot_normal', 'test_screenshot-browser.png').isfile()


@mock.patch('pytest_splinter.plugin.splinter.Browser')
@mock.patch.object(Config, 'warn', autospec=True)
def test_browser_screenshot_error(mocked_warn, mocked_browser, testdir):
    """Test warning with error during taking screenshots on test failure."""
    mocked_browser.return_value.driver.save_screenshot.side_effect = Exception('Failed')
    mocked_browser.return_value.driver_name = 'firefox'
    testdir.inline_runsource("""
        def test_screenshot(browser):
            assert False
    """, "-vvl", "-r w", "--splinter-session-scoped-browser=false")
    mocked_warn.assert_called_with(mock.ANY, 'SPL504', 'Could not save screenshot: Failed')


@pytest.mark.skipif('not config.pluginmanager.getplugin("xdist")', reason='pytest-xdist is not installed')
def test_browser_screenshot_xdist(testdir):
    """Test making screenshots on test failure in distributed mode (xdist).

    Distributed test run.
    """
    testdir.inline_runsource("""
        def test_screenshot(browser):
            assert False
    """, "-vl", "-n1")

    assert testdir.tmpdir.join('test_browser_screenshot_xdist', 'test_screenshot-browser.png').isfile()
