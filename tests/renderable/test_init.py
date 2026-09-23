from importlib import reload
from unittest.mock import patch

from textual_image._terminal import CellSize, TerminalCapabilities


def test_determining_best_renderable() -> None:
    from textual_image.renderable import halfcell, iterm2, select_image_class, sixel, tgp, unicode

    sixel_capabilities = TerminalCapabilities(CellSize(10, 20), sixel=True, tgp=True)
    tgp_capabilities = TerminalCapabilities(CellSize(10, 20), sixel=False, tgp=True)
    no_capabilities = TerminalCapabilities(CellSize(10, 20), sixel=False, tgp=False)

    with patch("sys.__stdout__.isatty", return_value=True):
        with patch("textual_image.renderable.iterm2.query_terminal_support", return_value=True):
            assert select_image_class(no_capabilities) is iterm2.Image

        with patch("textual_image.renderable.iterm2.query_terminal_support", return_value=False):
            assert select_image_class(sixel_capabilities) is sixel.Image
            assert select_image_class(tgp_capabilities) is tgp.Image
            assert select_image_class(no_capabilities) is halfcell.Image

    with patch("sys.__stdout__.isatty", return_value=False):
        assert select_image_class(no_capabilities) is unicode.Image


def test_imports_do_not_probe_terminal() -> None:
    import textual_image.renderable
    import textual_image.widget

    with patch("textual_image._terminal.probe_terminal") as probe:
        reload(textual_image.renderable)
        reload(textual_image.widget)

    probe.assert_not_called()
