from __future__ import annotations

from typing import List

from ..help import reload

reload("src", ["contexts", "events", "startup", "common"])
reload("src.commands")

from . import common as common
from .events import *
from .contexts import *
from .commands import *

__all__: List[str] = [
    # common
    "common",

    # handlers
    "BookmarkIdxInputHandler",
    "BookmarkTypeInputHandler",
    "BookmarkNameInputHandler",

    # commands
    "HyperhelpFocusCommand",
    "HyperhelpTopicCommand",
    "HyperhelpOpenBookmarkCommand",
    "HyperhelpPromptCreateBookmarkCommand",
    "HyperhelpContextCreateBookmarkCommand",
    "HyperhelpCreateBookmarkCommand",
    "HyperhelpContentsCommand",
    "HyperhelpIndexCommand",
    "HyperhelpNavigateCommand",
    "HyperHelpAboutCommand",
    "HyperhelpCurrentHelpCommand",
    "HyperhelpHistoryCommand",

    # internal commands
    "HyperhelpInternalProcessHeaderCommand",
    "HyperhelpInternalProcessCommentsCommand",
    "HyperhelpInternalProcessAnchorsCommand",
    "HyperhelpInternalProcessLinksCommand",
    "HyperhelpInternalFlagLinksCommand",

    # events/contexts
    "HyperhelpEventListener",
    "HyperhelpContextListener",
]
