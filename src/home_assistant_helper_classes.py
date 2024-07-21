"""

"""
from types import CodeType
import jinja2
from typing import Any, Mapping


class ScriptVariables:
    """Class to hold and render script variables."""

    def __init__(self, variables: dict[str, Any]) -> None:
        """Initialize script variables."""
        self.variables = variables
        self._has_template: bool | None = None

    def as_dict(self) -> dict[str, Any]:
        """Return dict version of this class."""
        return self.variables


def is_template_string(maybe_template: str) -> bool:
    """Check if the input is a Jinja2 template."""
    return "{" in maybe_template and (
        "{%" in maybe_template or "{{" in maybe_template or "{#" in maybe_template
    )


class Template:
    """Class to hold a template and manage caching and rendering."""

    __slots__ = (
        "__weakref__",
        "template",
        "hass",
        "is_static",
        "_compiled_code",
        "_compiled",
        "_exc_info",
        "_limited",
        "_strict",
        "_log_fn",
        "_hash_cache",
        "_renders",
    )

    def __init__(self, template: str) -> None:
        """Instantiate a template."""
        if not isinstance(template, str):
            raise TypeError("Expected template to be a string")

        self.template: str = template.strip()
        self._compiled_code: CodeType | None = None
        self._compiled: jinja2.Template | None = None
        self.is_static = not is_template_string(template)
        self._exc_info: sys._OptExcInfo | None = None
        self._limited: bool | None = None
        self._strict: bool | None = None
        self._log_fn: Callable[[int, str], None] | None = None
        self._hash_cache: int = hash(self.template)
        self._renders: int = 0

    @property
    def _env(self) -> TemplateEnvironment:
        if self.hass is None:
            return _NO_HASS_ENV
        # Bypass cache if a custom log function is specified
        if self._log_fn is not None:
            return TemplateEnvironment(
                self.hass, self._limited, self._strict, self._log_fn
            )
        if self._limited:
            wanted_env = _ENVIRONMENT_LIMITED
        elif self._strict:
            wanted_env = _ENVIRONMENT_STRICT
        else:
            wanted_env = _ENVIRONMENT
        if (ret := self.hass.data.get(wanted_env)) is None:
            ret = self.hass.data[wanted_env] = TemplateEnvironment(
                self.hass, self._limited, self._strict, self._log_fn
            )
        return ret

    def ensure_valid(self) -> None:
        """Return if template is valid."""
        if self.is_static or self._compiled_code is not None:
            return

        if compiled := self._env.template_cache.get(self.template):
            self._compiled_code = compiled
            return

        with _template_context_manager as cm:
            cm.set_template(self.template, "compiling")
            try:
                self._compiled_code = self._env.compile(self.template)
            except jinja2.TemplateError as err:
                raise TemplateError(err) from err

    def render(
        self,
        variables: TemplateVarsType = None,
        parse_result: bool = True,
        limited: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Render given template.

        If limited is True, the template is not allowed to access any function
        or filter depending on hass or the state machine.
        """
        if self.is_static:
            if not parse_result or self.hass and self.hass.config.legacy_templates:
                return self.template
            return self._parse_result(self.template)
        assert self.hass is not None, "hass variable not set on template"
        return run_callback_threadsafe(
            self.hass.loop,
            partial(self.async_render, variables, parse_result, limited, **kwargs),
        ).result()

    @callback
    def async_render(
        self,
        variables: TemplateVarsType = None,
        parse_result: bool = True,
        limited: bool = False,
        strict: bool = False,
        log_fn: Callable[[int, str], None] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Render given template.

        This method must be run in the event loop.

        If limited is True, the template is not allowed to access any function
        or filter depending on hass or the state machine.
        """
        self._renders += 1

        if self.is_static:
            if not parse_result or self.hass and self.hass.config.legacy_templates:
                return self.template
            return self._parse_result(self.template)

        compiled = self._compiled or self._ensure_compiled(limited, strict, log_fn)

        if variables is not None:
            kwargs.update(variables)

        try:
            render_result = _render_with_context(self.template, compiled, **kwargs)
        except Exception as err:
            raise TemplateError(err) from err

        render_result = render_result.strip()

        if not parse_result or self.hass and self.hass.config.legacy_templates:
            return render_result

        return self._parse_result(render_result)

    def _parse_result(self, render_result: str) -> Any:
        """Parse the result."""
        try:
            return _cached_parse_result(render_result)
        except (ValueError, TypeError, SyntaxError, MemoryError):
            pass

        return render_result

    async def async_render_will_timeout(
        self,
        timeout: float,
        variables: TemplateVarsType = None,
        strict: bool = False,
        log_fn: Callable[[int, str], None] | None = None,
        **kwargs: Any,
    ) -> bool:
        """Check to see if rendering a template will timeout during render.

        This is intended to check for expensive templates
        that will make the system unstable.  The template
        is rendered in the executor to ensure it does not
        tie up the event loop.

        This function is not a security control and is only
        intended to be used as a safety check when testing
        templates.

        This method must be run in the event loop.
        """
        self._renders += 1

        if self.is_static:
            return False

        compiled = self._compiled or self._ensure_compiled(strict=strict, log_fn=log_fn)

        if variables is not None:
            kwargs.update(variables)

        self._exc_info = None
        finish_event = asyncio.Event()

        def _render_template() -> None:
            assert self.hass is not None, "hass variable not set on template"
            try:
                _render_with_context(self.template, compiled, **kwargs)
            except TimeoutError:
                pass
            except Exception:  # noqa: BLE001
                self._exc_info = sys.exc_info()
            finally:
                self.hass.loop.call_soon_threadsafe(finish_event.set)

        try:
            template_render_thread = ThreadWithException(target=_render_template)
            template_render_thread.start()
            async with asyncio.timeout(timeout):
                await finish_event.wait()
            if self._exc_info:
                raise TemplateError(self._exc_info[1].with_traceback(self._exc_info[2]))
        except TimeoutError:
            template_render_thread.raise_exc(TimeoutError)
            return True
        finally:
            template_render_thread.join()

        return False

    @callback
    def async_render_to_info(
        self,
        variables: TemplateVarsType = None,
        strict: bool = False,
        log_fn: Callable[[int, str], None] | None = None,
        **kwargs: Any,
    ) -> RenderInfo:
        """Render the template and collect an entity filter."""
        if self.hass and self.hass.config.debug:
            self.hass.verify_event_loop_thread("async_render_to_info")
        self._renders += 1

        render_info = RenderInfo(self)

        if not self.hass:
            raise RuntimeError(f"hass not set while rendering {self}")

        if _render_info.get() is not None:
            raise RuntimeError(
                f"RenderInfo already set while rendering {self}, "
                "this usually indicates the template is being rendered "
                "in the wrong thread"
            )

        if self.is_static:
            render_info._result = self.template.strip()  # noqa: SLF001
            render_info._freeze_static()  # noqa: SLF001
            return render_info

        token = _render_info.set(render_info)
        try:
            render_info._result = self.async_render(  # noqa: SLF001
                variables, strict=strict, log_fn=log_fn, **kwargs
            )
        except TemplateError as ex:
            render_info.exception = ex
        finally:
            _render_info.reset(token)

        render_info._freeze()  # noqa: SLF001
        return render_info

    def render_with_possible_json_value(self, value, error_value=_SENTINEL):
        """Render template with value exposed.

        If valid JSON will expose value_json too.
        """
        if self.is_static:
            return self.template

        return run_callback_threadsafe(
            self.hass.loop,
            self.async_render_with_possible_json_value,
            value,
            error_value,
        ).result()

    @callback
    def async_render_with_possible_json_value(
        self,
        value: Any,
        error_value: Any = _SENTINEL,
        variables: dict[str, Any] | None = None,
        parse_result: bool = False,
    ) -> Any:
        """Render template with value exposed.

        If valid JSON will expose value_json too.

        This method must be run in the event loop.
        """
        self._renders += 1

        if self.is_static:
            return self.template

        compiled = self._compiled or self._ensure_compiled()

        variables = dict(variables or {})
        variables["value"] = value

        try:  # noqa: SIM105 - suppress is much slower
            variables["value_json"] = json_loads(value)
        except JSON_DECODE_EXCEPTIONS:
            pass

        try:
            render_result = _render_with_context(
                self.template, compiled, **variables
            ).strip()
        except jinja2.TemplateError as ex:
            if error_value is _SENTINEL:
                _LOGGER.error(
                    "Error parsing value: %s (value: %s, template: %s)",
                    ex,
                    value,
                    self.template,
                )
            return value if error_value is _SENTINEL else error_value

        if not parse_result or self.hass and self.hass.config.legacy_templates:
            return render_result

        return self._parse_result(render_result)

    def _ensure_compiled(
        self,
        limited: bool = False,
        strict: bool = False,
        log_fn: Callable[[int, str], None] | None = None,
    ) -> jinja2.Template:
        """Bind a template to a specific hass instance."""
        self.ensure_valid()

        assert self.hass is not None, "hass variable not set on template"
        assert (
            self._limited is None or self._limited == limited
        ), "can't change between limited and non limited template"
        assert (
            self._strict is None or self._strict == strict
        ), "can't change between strict and non strict template"
        assert not (strict and limited), "can't combine strict and limited template"
        assert (
            self._log_fn is None or self._log_fn == log_fn
        ), "can't change custom log function"
        assert self._compiled_code is not None, "template code was not compiled"

        self._limited = limited
        self._strict = strict
        self._log_fn = log_fn
        env = self._env

        self._compiled = jinja2.Template.from_code(
            env, self._compiled_code, env.globals, None
        )

        return self._compiled

    def __eq__(self, other):
        """Compare template with another."""
        return (
            self.__class__ == other.__class__
            and self.template == other.template
            and self.hass == other.hass
        )

    def __hash__(self) -> int:
        """Hash code for template."""
        return self._hash_cache

    def __repr__(self) -> str:
        """Representation of Template."""
        return f"Template<template=({self.template}) renders={self._renders}>"


@cache
def _domain_states(hass: HomeAssistant, name: str) -> DomainStates:
    return DomainStates(hass, name)


def _readonly(*args: Any, **kwargs: Any) -> Any:
    """Raise an exception when a states object is modified."""
    raise RuntimeError(f"Cannot modify template States object: {args} {kwargs}")
