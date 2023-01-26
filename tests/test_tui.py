from lockhart.tui.app import RequestApp


async def test_run_app():
    async with RequestApp().run_test() as request_app:
        assert request_app.app._running


async def test_press_next():
    async with RequestApp().run_test() as request_app:
        await request_app.press("j")
        assert request_app.app.i == 1
        await request_app.press("j")
        assert request_app.app.i == 2
        await request_app.press("j")
        assert request_app.app.i == 3


async def test_press_prev():
    async with RequestApp().run_test() as request_app:
        await request_app.press("k")
        assert request_app.app.i == len(request_app.app.history) - 1
        await request_app.press("k")
        assert request_app.app.i == len(request_app.app.history) - 2
        await request_app.press("k")
        assert request_app.app.i == len(request_app.app.history) - 3


async def test_press_next_rollover():
    async with RequestApp().run_test() as request_app:
        for _ in range(len(request_app.app.history)):
            await request_app.press("j")
        assert request_app.app.i == 0


async def test_press_prev_rollover():
    async with RequestApp().run_test() as request_app:
        for _ in range(len(request_app.app.history)):
            await request_app.press("k")
        assert request_app.app.i == 0


# async def test_mount_request():
#     async with RequestApp().run_test() as request_app:
#         request_app.mount(Request())
