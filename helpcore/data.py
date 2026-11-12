from __future__ import annotations

from typing import Dict, List, NamedTuple, Optional, Tuple, TypedDict


###----------------------------------------------------------------------------


class _HelpTopicRequired(TypedDict):
    topic: str
    caption: str
    file: str


class HelpTopic(_HelpTopicRequired, total=False):
    children: List[HelpTopic]


class HelpTocEntry(_HelpTopicRequired, total=False):
    children: List[HelpTocEntry]


class LinkInfo(TypedDict):
    pkg: Optional[str]
    topic: str


# A representation of the data that was contained in a hyperhelp help document
# header. This is used to construct a more human readable header.
class HeaderData(NamedTuple):
    file: str
    title: str
    date: float


# A representation of a history node that tracks what help topics have been
# viewed and where the viewport was left.
class HistoryData(NamedTuple):
    package: Optional[str]
    file: Optional[str]
    viewport: Tuple[float, float]
    caret: Tuple[int, int]


# A representation of all of the help available for a particular package.
#
# This tells us all of the information we need about the help for a package at
# load time so that we don't need to look it up later.
class HelpData(NamedTuple):
    package: str
    index_file: str
    description: str
    doc_root: str
    help_topics: Dict[str, HelpTopic]
    help_aliases: Dict[str, str]
    help_files: Dict[str, str]
    package_files: List[str]
    urls: List[str]
    help_toc: List[HelpTocEntry]


###----------------------------------------------------------------------------
