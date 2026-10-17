from ....help import reload

reload("src.commands.internal", ["common", "flag_links", "process_anchors",
       "process_comments", "process_header", "process_links"])

from .flag_links import HyperhelpInternalFlagLinksCommand
from .process_anchors import HyperhelpInternalProcessAnchorsCommand
from .process_comments import HyperhelpInternalProcessCommentsCommand
from .process_header import HyperhelpInternalProcessHeaderCommand
from .process_links import HyperhelpInternalProcessLinksCommand

__all__ = [
    # internal commands
    "HyperhelpInternalProcessHeaderCommand",
    "HyperhelpInternalProcessCommentsCommand",
    "HyperhelpInternalProcessAnchorsCommand",
    "HyperhelpInternalProcessLinksCommand",
    "HyperhelpInternalFlagLinksCommand",
]
