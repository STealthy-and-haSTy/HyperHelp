import sublime

from .voluptuous import Schema, Required, Optional, Any, Invalid, MultipleInvalid

from .common import log


###----------------------------------------------------------------------------


# The schema to validate that a topic dictionary is properly formatted.
_topic_schema = Schema({
    Required("topic"): str,
    Optional("caption"): str,

    # Aliases must be an array of strings
    Optional("aliases"): [str]
})

def _validate_hybrid_array(v):
    """
    Custom validator for the "Hybrid Array" used in help_files and externals.

    The array must not be empty. The first item in the array must be a string
    (typically a file path or URL), and the remainder must be topic
    dictionaries.
    """
    if not isinstance(v, list):
        raise Invalid("expected a list")
    if len(v) == 0:
        raise Invalid("list must not be empty")

    # The first item MUST be a string
    if not isinstance(v[0], str):
        raise Invalid("first element must be a string", path=[0])

    # Validate the remainder of the array elements as topic dictionaries and
    # preserve the exact path to any failure so the index is reported.
    for i in range(1, len(v)):
        try:
            _topic_schema(v[i])
        except MultipleInvalid as e:
            # prepend the array index to the error path so it reports
            # correctly.
            for error in e.errors:
                error.prepend([i])
            raise e
        except Invalid as e:
            e.prepend([i])
            raise e

    return v

def _validate_help_contents(v):
    """
    Recursive validator for the help table of contents in the "help_contents"
    key of the help index.

    Items must be topic dictionaries or strings. Topic dictionaries require a
    topic key but may also contain a caption key and a children key which is an
    array that is recursively identical to this one.

    Values that are strings are expanded at runtime to be topic dictionaries
    with no children and an inherited caption.
    """
    if not isinstance(v, list):
        raise Invalid("expected a list")

    node = Any(
        str,
        Schema({
            Required("topic"): str,
            Optional("caption"): str,

            # This is recursive; it points back to this exact function
            Optional("children"): _validate_help_contents
        })
    )

    # Schema([node]) automatically handles validating the list and tracking
    # index paths for error reporting.
    return Schema([node])(v)

# The overall schema used to validate a hyperhelp index file.
_index_schema = Schema({
    Required("package"): str,
    Optional("description"): str,
    Optional("doc_root"): str,
    Optional("default_caption"): str,

    # Any string key is allowed, but all must have values which are Hybrid
    # Arrays (first item string, remainder topic dicts).
    Required("help_files"): Schema({str: _validate_hybrid_array}),

    # The table of contents structure is optional
    Optional("help_contents"): _validate_help_contents,

    # Externals behave exactly like help_files structurally
    Optional("externals"): Schema({str: _validate_hybrid_array})
})



###----------------------------------------------------------------------------


def validate_index(content, index_res):
    """
    Given a raw JSON string that represents a help index for a package, perform
    validation on it to ensure that it's valid JSON and also that it conforms
    to the appropriate index file help schema.

    Return a decoded dict object on success or None on failure.
    """
    def validate_fail(message, *args):
        log("Error validating index in '%s': %s", index_res, message % args)

    try:
        log("Loading help index from '%s'", index_res)
        raw_dict = sublime.decode_value(content)
    except:
        return validate_fail("Invalid JSON detected; unable to decode")

    try:
        _index_schema(raw_dict)
        return raw_dict

    except MultipleInvalid as error:
        # Voluptuous aggregates errors. We can grab the first one or loop them.
        # path is a list of keys/indexes leading to the exact failure
        path = "".join(f"[{repr(p)}]" for p in error.path)
        return validate_fail("at %s: %s", path, error.msg)

    # Catch any underlying structural execution errors (e.g., if a custom
    # function like _validate_hybrid_array explodes due to unexpected types)
    except Exception as error:
        return validate_fail("%s", error)


###----------------------------------------------------------------------------
