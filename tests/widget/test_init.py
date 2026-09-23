from unittest import skipUnless
from unittest.mock import patch

from tests.data import TEXTUAL_ENABLED


@skipUnless(TEXTUAL_ENABLED, "Textual support disabled")
def test_determining_best_widget() -> None:
    from textual_image.renderable.halfcell import Image as HalfcellRenderable
    from textual_image.renderable.iterm2 import Image as ITerm2Renderable
    from textual_image.renderable.sixel import Image as SixelRenderable
    from textual_image.renderable.tgp import Image as TGPRenderable
    from textual_image.renderable.unicode import Image as UnicodeRenderable
    from textual_image.widget import HalfcellImage, ITerm2Image, TGPImage, UnicodeImage, select_image_class
    from textual_image.widget.sixel import Image as SixelImage

    expected = {
        ITerm2Renderable: ITerm2Image,
        SixelRenderable: SixelImage,
        TGPRenderable: TGPImage,
        UnicodeRenderable: UnicodeImage,
        HalfcellRenderable: HalfcellImage,
    }
    for renderable, widget in expected.items():
        with patch("textual_image.widget.select_renderable_class", return_value=renderable):
            assert select_image_class() is widget
