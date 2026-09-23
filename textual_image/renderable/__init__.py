"""Rich renderables to display images in terminal."""

import logging
import sys
from typing import Type, TypeAlias

from textual_image._terminal import TerminalCapabilities, probe_terminal
from textual_image.renderable import iterm2
from textual_image.renderable.halfcell import Image as HalfcellImage
from textual_image.renderable.iterm2 import Image as ITerm2Image
from textual_image.renderable.sixel import Image as SixelImage
from textual_image.renderable.tgp import Image as TGPImage
from textual_image.renderable.unicode import Image as UnicodeImage

logger = logging.getLogger(__name__)

ImageType: TypeAlias = Type[TGPImage | ITerm2Image | SixelImage | HalfcellImage | UnicodeImage]


def select_image_class(capabilities: TerminalCapabilities | None = None) -> ImageType:
    """Select the best renderable, probing synchronously when needed.

    Pass externally detected capabilities when another event loop owns stdin.

    Args:
        capabilities: Previously detected terminal capabilities.

    Returns:
        The selected renderable class.
    """
    if not sys.__stdout__ or not sys.__stdout__.isatty():
        logger.debug("Not connected to a terminal, falling back to unicode")
        return UnicodeImage
    if iterm2.query_terminal_support():
        logger.debug("iTerm2 support detected")
        return ITerm2Image

    capabilities = capabilities or probe_terminal()
    if capabilities.sixel:
        logger.debug("Sixel support detected")
        return SixelImage
    if capabilities.tgp:
        logger.debug("Terminal Graphics Protocol support detected")
        return TGPImage

    logger.debug("Connected to a terminal, using half cell rendering")
    return HalfcellImage


# Importing this module must not read stdin. Applications can replace this
# fallback with select_image_class() after their terminal driver has started.
Image: ImageType = HalfcellImage if sys.__stdout__ and sys.__stdout__.isatty() else UnicodeImage

__all__ = [
    "Image",
    "ImageType",
    "select_image_class",
    "TGPImage",
    "SixelImage",
    "ITerm2Image",
    "HalfcellImage",
    "UnicodeImage",
]
