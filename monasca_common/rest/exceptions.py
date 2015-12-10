class UnsupportedContentTypeException(Exception):
    """Exception thrown if content type is not supported."""
    pass


class UnreadableContentError(IOError):
    """Exception thrown if reading data fails

    :py:class`.UnreadableContentError` may be thrown
    if data was impossible to read from input

    """
    pass


class DataConversionException(Exception):
    """Exception thrown if data transformation fails

    :py:class`.DataConversionException` may be thrown
    if data was impossible to transform into target
    representation according to content_type classifier.

    """
    pass
