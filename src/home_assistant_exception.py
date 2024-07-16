from typing import TYPE_CHECKING, Callable

_function_cache: dict[str, Callable[[str, str, dict[str, str] | None], str]] = {}

class HomeAssistantError(Exception):
    """General Home Assistant exception occurred."""

    _message: str | None = None
    generate_message: bool = False

    def __init__(
        self,
        *args: object,
        translation_domain: str | None = None,
        translation_key: str | None = None,
        translation_placeholders: dict[str, str] | None = None,
    ) -> None:
        """Initialize exception."""
        if not args and translation_key and translation_domain:
            self.generate_message = True
            args = (translation_key,)

        super().__init__(*args)
        self.translation_domain = translation_domain
        self.translation_key = translation_key
        self.translation_placeholders = translation_placeholders

    def __str__(self) -> str:
        """Return exception message.

        If no message was passed to `__init__`, the exception message is generated from
        the translation_key. The message will be in English, regardless of the configured
        language.
        """

        if self._message:
            return self._message

        if not self.generate_message:
            self._message = super().__str__()
            return self._message

        if TYPE_CHECKING:
            assert self.translation_key is not None
            assert self.translation_domain is not None

        self._message = _function_cache["async_get_exception_message"](
            self.translation_domain, self.translation_key, self.translation_placeholders
        )
        return self._message
    
