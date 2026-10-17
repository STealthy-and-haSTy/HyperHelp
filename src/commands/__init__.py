from ...help import reload

reload("src.commands", ["common", "about", "contents", "create_bookmark",
       "current_help", "focus", "history", "index", "navigate", "open_bookmark",
       "prompt_create_bookmark", "context_create_bookmark", "topic"])
reload("src.commands.internal")

from .common import BookmarkIdxInputHandler, BookmarkTypeInputHandler, BookmarkNameInputHandler

from .internal import *

from .about import HyperHelpAboutCommand
from .contents import HyperhelpContentsCommand
from .create_bookmark import HyperhelpCreateBookmarkCommand
from .current_help import HyperhelpCurrentHelpCommand
from .focus import HyperhelpFocusCommand
from .history import HyperhelpHistoryCommand
from .index import HyperhelpIndexCommand
from .navigate import HyperhelpNavigateCommand
from .open_bookmark import HyperhelpOpenBookmarkCommand
from .prompt_create_bookmark import HyperhelpPromptCreateBookmarkCommand
from .context_create_bookmark import HyperhelpContextCreateBookmarkCommand
from .topic import HyperhelpTopicCommand


__all__ = [
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
]
