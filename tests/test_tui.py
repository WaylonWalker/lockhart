from unittest.mock import patch

from lockhart.tui.app import RequestApp


async def test_run_app(load_history):
    async with RequestApp().run_test() as request_app:
        assert request_app.app._running
        assert load_history.call_count == 1


async def test_press_next(load_history):
    async with RequestApp().run_test() as request_app:
        await request_app.press("j")
        assert request_app.app.i == 1
        await request_app.press("j")
        assert request_app.app.i == 2
        await request_app.press("j")
        assert request_app.app.i == 3
        assert load_history.call_count == 1
        assert load_history.called_with()


async def test_press_prev(load_history):
    async with RequestApp().run_test() as request_app:
        await request_app.press("k")
        assert request_app.app.i == len(request_app.app.history) - 1
        await request_app.press("k")
        assert request_app.app.i == len(request_app.app.history) - 2
        await request_app.press("k")
        assert request_app.app.i == len(request_app.app.history) - 3
        assert load_history.call_count == 1
        assert load_history.called_with()


async def test_press_next_rollover(load_history):
    async with RequestApp().run_test() as request_app:
        for _ in range(len(request_app.app.history)):
            await request_app.press("j")
        assert request_app.app.i == 0
        assert load_history.call_count == 1
        assert load_history.called_with()


async def test_copy_to_clipboard(load_history):
    async with RequestApp().run_test() as request_app:
        with patch(
            "lockhart.tui.app.Request.copy_to_clipboard"
        ) as mock_copy_to_clipboard:
            await request_app.press("c")
            assert load_history.call_count == 1
            assert load_history.called_with()
            assert mock_copy_to_clipboard.call_count == 1
            assert mock_copy_to_clipboard.called_with()


async def test_toggle_dark(load_history):
    async with RequestApp().run_test() as request_app:
        assert request_app.app.dark
        await request_app.press("d")
        assert not request_app.app.dark
        assert load_history.call_count == 1
        assert load_history.called_with()
