"""Textual `Widget` to display images in terminal."""

from typing import Type, TypeAlias

from textual_image._terminal import TerminalCapabilities
from textual_image.renderable import Image as DefaultRenderable
from textual_image.renderable import select_image_class as select_renderable_class
from textual_image.renderable.halfcell import Image as HalfcellRenderable
from textual_image.renderable.iterm2 import Image as ITerm2Renderable
from textual_image.renderable.sixel import Image as SixelRenderable
from textual_image.renderable.sixel import SixelOptions
from textual_image.renderable.tgp import Image as TGPRenderable
from textual_image.renderable.unicode import Image as UnicodeRenderable
from textual_image.widget._base import Image as BaseImage
from textual_image.widget.iterm2 import Image as ITerm2Image
from textual_image.widget.sixel import Image as SixelImage


class TGPImage(BaseImage, Renderable=TGPRenderable):
    """Textual `Widget` to render images in the terminal using the Terminal Graphics Protocol (<https://sw.kovidgoyal.net/kitty/graphics-protocol/>)."""

    pass


class HalfcellImage(BaseImage, Renderable=HalfcellRenderable):
    """Textual `Widget` to render images in the terminal using colored half cells."""

    pass


class UnicodeImage(BaseImage, Renderable=UnicodeRenderable):
    """Textual `Widget` to render images in the terminal using unicode characters."""

    pass


ImageType: TypeAlias = Type[TGPImage | SixelImage | ITerm2Image | HalfcellImage | UnicodeImage]


def select_image_class(capabilities: TerminalCapabilities | None = None) -> ImageType:
    """Select the best image widget, probing synchronously when needed.

    Pass externally detected capabilities when another event loop owns stdin.

    Args:
        capabilities: Previously detected terminal capabilities.

    Returns:
        The selected widget class.
    """
    renderable = select_renderable_class(capabilities)
    if renderable is ITerm2Renderable:
        return ITerm2Image
    if renderable is SixelRenderable:
        return SixelImage
    if renderable is TGPRenderable:
        return TGPImage
    if renderable is UnicodeRenderable:
        return UnicodeImage
    return HalfcellImage


# Safe default; call select_image_class() after terminal capabilities are known.
Image: ImageType = UnicodeImage if DefaultRenderable is UnicodeRenderable else HalfcellImage


__all__ = [
    "Image",
    "ImageType",
    "select_image_class",
    "TGPImage",
    "SixelImage",
    "SixelOptions",
    "ITerm2Image",
    "HalfcellImage",
    "UnicodeImage",
]
