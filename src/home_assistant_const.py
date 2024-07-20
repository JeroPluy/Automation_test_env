from typing import Any, Final, Mapping
from enum import StrEnum
import voluptuous as vol
import re


TIME_PERIOD_ERROR = "offset {} should be format 'HH:MM', 'HH:MM:SS' or 'HH:MM:SS.F'"

# Entity target all constant
ENTITY_MATCH_NONE: Final = "none"
ENTITY_MATCH_ALL: Final = "all"
ENTITY_MATCH_ANY: Final = "any"

# Entity target domain constant
_OBJECT_ID = r"(?!_)[\da-z_]+(?<!_)"
_DOMAIN = r"(?!.+__)" + _OBJECT_ID
VALID_ENTITY_ID = re.compile(r"^" + _DOMAIN + r"\." + _OBJECT_ID + r"$")

WEEKDAYS: Final[list[str]] = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# Contains one string or a list of strings, each being an entity id
ATTR_ENTITY_ID: Final = "entity_id"

# Contains one string or a list of strings, each being an area id
ATTR_AREA_ID: Final = "area_id"

# Contains one string, the device ID
ATTR_DEVICE_ID: Final = "device_id"

# Contains one string or a list of strings, each being an floor id
ATTR_FLOOR_ID: Final = "floor_id"

# Contains one string or a list of strings, each being an label id
ATTR_LABEL_ID: Final = "label_id"

# Sun events
SUN_EVENT_SUNSET: Final = "sunset"
SUN_EVENT_SUNRISE: Final = "sunrise"

# #### CONFIG ####
CONF_ABOVE: Final = "above"
# CONF_ACCESS_TOKEN: Final = "access_token"
# CONF_ADDRESS: Final = "address"
# CONF_AFTER: Final = "after"
CONF_ALIAS: Final = "alias"
# CONF_LLM_HASS_API = "llm_hass_api"
# CONF_ALLOWLIST_EXTERNAL_URLS: Final = "allowlist_external_urls"
# CONF_API_KEY: Final = "api_key"
# CONF_API_TOKEN: Final = "api_token"
# CONF_API_VERSION: Final = "api_version"
# CONF_ARMING_TIME: Final = "arming_time"
# CONF_AT: Final = "at"
CONF_ATTRIBUTE: Final = "attribute"
# CONF_AUTH_MFA_MODULES: Final = "auth_mfa_modules"
# CONF_AUTH_PROVIDERS: Final = "auth_providers"
# CONF_AUTHENTICATION: Final = "authentication"
# CONF_BASE: Final = "base"
# CONF_BEFORE: Final = "before"
CONF_BELOW: Final = "below"
# CONF_BINARY_SENSORS: Final = "binary_sensors"
# CONF_BRIGHTNESS: Final = "brightness"
# CONF_BROADCAST_ADDRESS: Final = "broadcast_address"
# CONF_BROADCAST_PORT: Final = "broadcast_port"
CONF_CHOOSE: Final = "choose"
# CONF_CLIENT_ID: Final = "client_id"
# CONF_CLIENT_SECRET: Final = "client_secret"
# CONF_CODE: Final = "code"
# CONF_COLOR_TEMP: Final = "color_temp"
# CONF_COMMAND: Final = "command"
# CONF_COMMAND_CLOSE: Final = "command_close"
# CONF_COMMAND_OFF: Final = "command_off"
# CONF_COMMAND_ON: Final = "command_on"
# CONF_COMMAND_OPEN: Final = "command_open"
# CONF_COMMAND_STATE: Final = "command_state"
# CONF_COMMAND_STOP: Final = "command_stop"
CONF_CONDITION: Final = "condition"
CONF_CONDITIONS: Final = "conditions"
CONF_CONTINUE_ON_ERROR: Final = "continue_on_error"
CONF_CONTINUE_ON_TIMEOUT: Final = "continue_on_timeout"
CONF_COUNT: Final = "count"
# CONF_COUNTRY: Final = "country"
# CONF_COUNTRY_CODE: Final = "country_code"
# CONF_COVERS: Final = "covers"
# CONF_CURRENCY: Final = "currency"
# CONF_CUSTOMIZE: Final = "customize"
# CONF_CUSTOMIZE_DOMAIN: Final = "customize_domain"
# CONF_CUSTOMIZE_GLOB: Final = "customize_glob"
CONF_DEFAULT: Final = "default"
CONF_DELAY: Final = "delay"
# CONF_DELAY_TIME: Final = "delay_time"
CONF_DESCRIPTION: Final = "description"
# CONF_DEVICE: Final = "device"
# CONF_DEVICES: Final = "devices"
# CONF_DEVICE_CLASS: Final = "device_class"
CONF_DEVICE_ID: Final = "device_id"
# CONF_DISARM_AFTER_TRIGGER: Final = "disarm_after_trigger"
# CONF_DISCOVERY: Final = "discovery"
# CONF_DISKS: Final = "disks"
# CONF_DISPLAY_CURRENCY: Final = "display_currency"
# CONF_DISPLAY_OPTIONS: Final = "display_options"
CONF_DOMAIN: Final = "domain"
# CONF_DOMAINS: Final = "domains"
# CONF_EFFECT: Final = "effect"
# CONF_ELEVATION: Final = "elevation"
CONF_ELSE: Final = "else"
# CONF_EMAIL: Final = "email"
CONF_ENABLED: Final = "enabled"
# CONF_ENTITIES: Final = "entities"
# CONF_ENTITY_CATEGORY: Final = "entity_category"
CONF_ENTITY_ID: Final = "entity_id"
CONF_ENTITY_NAMESPACE: Final = "entity_namespace"
# CONF_ENTITY_PICTURE_TEMPLATE: Final = "entity_picture_template"
CONF_ERROR: Final = "error"
CONF_EVENT: Final = "event"
CONF_EVENT_DATA: Final = "event_data"
CONF_EVENT_DATA_TEMPLATE: Final = "event_data_template"
# CONF_EXCLUDE: Final = "exclude"
# CONF_EXTERNAL_URL: Final = "external_url"
# CONF_FILENAME: Final = "filename"
# CONF_FILE_PATH: Final = "file_path"
CONF_FOR: Final = "for"
CONF_FOR_EACH: Final = "for_each"
# CONF_FORCE_UPDATE: Final = "force_update"
# CONF_FRIENDLY_NAME: Final = "friendly_name"
# CONF_FRIENDLY_NAME_TEMPLATE: Final = "friendly_name_template"
# CONF_HEADERS: Final = "headers"
# CONF_HOST: Final = "host"
# CONF_HOSTS: Final = "hosts"
# CONF_HS: Final = "hs"
# CONF_ICON: Final = "icon"
# CONF_ICON_TEMPLATE: Final = "icon_template"
CONF_ID: Final = "id"
CONF_IF: Final = "if"
# CONF_INCLUDE: Final = "include"
# CONF_INTERNAL_URL: Final = "internal_url"
# CONF_IP_ADDRESS: Final = "ip_address"
# CONF_LANGUAGE: Final = "language"
# CONF_LATITUDE: Final = "latitude"
# CONF_LEGACY_TEMPLATES: Final = "legacy_templates"
# CONF_LIGHTS: Final = "lights"
# CONF_LOCATION: Final = "location"
# CONF_LONGITUDE: Final = "longitude"
# CONF_MAC: Final = "mac"
CONF_MATCH: Final = "match"
# CONF_MAXIMUM: Final = "maximum"
# CONF_MEDIA_DIRS: Final = "media_dirs"
# CONF_METHOD: Final = "method"
# CONF_MINIMUM: Final = "minimum"
CONF_MODE: Final = "mode"
# CONF_MODEL: Final = "model"
# CONF_MONITORED_CONDITIONS: Final = "monitored_conditions"
# CONF_MONITORED_VARIABLES: Final = "monitored_variables"
# CONF_NAME: Final = "name"
# CONF_OFFSET: Final = "offset"
# CONF_OPTIMISTIC: Final = "optimistic"
# CONF_PACKAGES: Final = "packages"
CONF_PARALLEL: Final = "parallel"
# CONF_PARAMS: Final = "params"
# CONF_PASSWORD: Final = "password"
# CONF_PATH: Final = "path"
# CONF_PAYLOAD: Final = "payload"
# CONF_PAYLOAD_OFF: Final = "payload_off"
# CONF_PAYLOAD_ON: Final = "payload_on"
# CONF_PENDING_TIME: Final = "pending_time"
# CONF_PIN: Final = "pin"
CONF_PLATFORM: Final = "platform"
# CONF_PORT: Final = "port"
# CONF_PREFIX: Final = "prefix"
# CONF_PROFILE_NAME: Final = "profile_name"
# CONF_PROTOCOL: Final = "protocol"
# CONF_PROXY_SSL: Final = "proxy_ssl"
# CONF_QUOTE: Final = "quote"
# CONF_RADIUS: Final = "radius"
# CONF_RECIPIENT: Final = "recipient"
# CONF_REGION: Final = "region"
CONF_REPEAT: Final = "repeat"
# CONF_RESOURCE: Final = "resource"
# CONF_RESOURCE_TEMPLATE: Final = "resource_template"
# CONF_RESOURCES: Final = "resources"
CONF_RESPONSE_VARIABLE: Final = "response_variable"
# CONF_RGB: Final = "rgb"
# CONF_ROOM: Final = "room"
CONF_SCAN_INTERVAL: Final = "scan_interval"
CONF_SCENE: Final = "scene"
# CONF_SELECTOR: Final = "selector"
# CONF_SENDER: Final = "sender"
# CONF_SENSORS: Final = "sensors"
# CONF_SENSOR_TYPE: Final = "sensor_type"
CONF_SEQUENCE: Final = "sequence"
CONF_SERVICE: Final = "service"
CONF_SERVICE_DATA: Final = "data"
CONF_SERVICE_DATA_TEMPLATE: Final = "data_template"
CONF_SERVICE_TEMPLATE: Final = "service_template"
CONF_SET_CONVERSATION_RESPONSE: Final = "set_conversation_response"
# CONF_SHOW_ON_MAP: Final = "show_on_map"
# CONF_SLAVE: Final = "slave"
# CONF_SOURCE: Final = "source"
# CONF_SSL: Final = "ssl"
CONF_STATE: Final = "state"
# CONF_STATE_TEMPLATE: Final = "state_template"
CONF_STOP: Final = "stop"
# CONF_STRUCTURE: Final = "structure"
# CONF_SWITCHES: Final = "switches"
CONF_TARGET: Final = "target"
# CONF_TEMPERATURE_UNIT: Final = "temperature_unit"
CONF_THEN: Final = "then"
CONF_TIMEOUT: Final = "timeout"
# CONF_TIME_ZONE: Final = "time_zone"
# CONF_TOKEN: Final = "token"
# CONF_TRIGGER_TIME: Final = "trigger_time"
# CONF_TTL: Final = "ttl"
# CONF_TYPE: Final = "type"
# CONF_UNIQUE_ID: Final = "unique_id"
# CONF_UNIT_OF_MEASUREMENT: Final = "unit_of_measurement"
# CONF_UNIT_SYSTEM: Final = "unit_system"
CONF_UNTIL: Final = "until"
# CONF_URL: Final = "url"
# CONF_USERNAME: Final = "username"
# CONF_UUID: Final = "uuid"
CONF_VALUE_TEMPLATE: Final = "value_template"
CONF_VARIABLES: Final = "variables"
# CONF_VERIFY_SSL: Final = "verify_ssl"
CONF_WAIT_FOR_TRIGGER: Final = "wait_for_trigger"
CONF_WAIT_TEMPLATE: Final = "wait_template"
# CONF_WEBHOOK_ID: Final = "webhook_id"
# CONF_WEEKDAY: Final = "weekday"
CONF_WHILE: Final = "while"
# CONF_WHITELIST: Final = "whitelist"
# CONF_ALLOWLIST_EXTERNAL_DIRS: Final = "allowlist_external_dirs"
# LEGACY_CONF_WHITELIST_EXTERNAL_DIRS: Final = "whitelist_external_dirs"
# CONF_DEBUG: Final = "debug"
# CONF_XY: Final = "xy"
# CONF_ZONE: Final = "zone"

# CONF_ACTION = "action"
# CONF_TRIGGER = "trigger"
# CONF_TRIGGER_VARIABLES = "trigger_variables"
# DOMAIN = "automation"
CONF_HIDE_ENTITY = "hide_entity"
# CONF_CONDITION_TYPE = "condition_type"
# CONF_INITIAL_STATE = "initial_state"
# CONF_BLUEPRINT = "blueprint"
# CONF_INPUT = "input"
# CONF_TRACE = "trace"

DEFAULT_INITIAL_STATE = True

# SCRIPT_MODE
SCRIPT_MODE_PARALLEL = "parallel"
SCRIPT_MODE_QUEUED = "queued"
SCRIPT_MODE_RESTART = "restart"
SCRIPT_MODE_SINGLE = "single"
SCRIPT_MODE_CHOICES = [
    SCRIPT_MODE_PARALLEL,
    SCRIPT_MODE_QUEUED,
    SCRIPT_MODE_RESTART,
    SCRIPT_MODE_SINGLE,
]

# INSTANCES
CONF_MAX = "max"
DEFAULT_MAX = 10
CONF_MAX_EXCEEDED = "max_exceeded"
_MAX_EXCEEDED_CHOICES = ["SILENT"]
DEFAULT_MAX_EXCEEDED = "WARNING"

# SCRIPT_ACTION
SCRIPT_ACTION_ACTIVATE_SCENE = "scene"
SCRIPT_ACTION_CALL_SERVICE = "call_service"
SCRIPT_ACTION_CHECK_CONDITION = "condition"
SCRIPT_ACTION_CHOOSE = "choose"
SCRIPT_ACTION_DELAY = "delay"
SCRIPT_ACTION_DEVICE_AUTOMATION = "device"
SCRIPT_ACTION_FIRE_EVENT = "event"
SCRIPT_ACTION_IF = "if"
SCRIPT_ACTION_PARALLEL = "parallel"
SCRIPT_ACTION_REPEAT = "repeat"
SCRIPT_ACTION_SEQUENCE = "sequence"
SCRIPT_ACTION_SET_CONVERSATION_RESPONSE = "set_conversation_response"
SCRIPT_ACTION_STOP = "stop"
SCRIPT_ACTION_VARIABLES = "variables"
SCRIPT_ACTION_WAIT_FOR_TRIGGER = "wait_for_trigger"
SCRIPT_ACTION_WAIT_TEMPLATE = "wait_template"

# AUTOMATION
CONF_ACTION = "action"
CONF_TRIGGER = "trigger"
CONF_TRIGGER_VARIABLES = "trigger_variables"
DOMAIN = "automation"

CONF_HIDE_ENTITY = "hide_entity"

CONF_CONDITION_TYPE = "condition_type"
CONF_INITIAL_STATE = "initial_state"
CONF_BLUEPRINT = "blueprint"
CONF_INPUT = "input"
CONF_TRACE = "trace"
CONF_STORED_TRACES = "stored_traces"
DEFAULT_STORED_TRACES = 5

# TYPES
type VolDictType = dict[str | vol.Marker, Any]
type VolSchemaType = vol.Schema | vol.All | vol.Any
type ConfigType = dict[str, Any]

class UnitOfTemperature(StrEnum):
    """Temperature units."""

    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    KELVIN = "K"

class NodeStrClass(str):
    """Wrapper class to be able to add attributes on a string."""

    __slots__ = ("__config_file__", "__line__")

    __config_file__: str
    __line__: int | str

    def __voluptuous_compile__(self, schema: vol.Schema) -> Any:
        """Needed because vol.Schema.compile does not handle str subclasses."""
        return _compile_scalar(self)  # type: ignore[no-untyped-call]

class ResultWrapper:
    """Result wrapper class to store render result."""

    render_result: str | None

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


# Home Assistant types
byte = vol.All(vol.Coerce(int), vol.Range(min=0, max=255))
small_float = vol.All(vol.Coerce(float), vol.Range(min=0, max=1))
positive_int = vol.All(vol.Coerce(int), vol.Range(min=0))
positive_float = vol.All(vol.Coerce(float), vol.Range(min=0))
latitude = vol.All(
    vol.Coerce(float), vol.Range(min=-90, max=90), msg="invalid latitude"
)
longitude = vol.All(
    vol.Coerce(float), vol.Range(min=-180, max=180), msg="invalid longitude"
)
gps = vol.ExactSequence([latitude, longitude])
sun_event = vol.All(vol.Lower, vol.Any(SUN_EVENT_SUNSET, SUN_EVENT_SUNRISE))
port = vol.All(vol.Coerce(int), vol.Range(min=1, max=65535))

COUNTRIES: Final[set[str]] = {
    "AD",
    "AE",
    "AF",
    "AG",
    "AI",
    "AL",
    "AM",
    "AO",
    "AQ",
    "AR",
    "AS",
    "AT",
    "AU",
    "AW",
    "AX",
    "AZ",
    "BA",
    "BB",
    "BD",
    "BE",
    "BF",
    "BG",
    "BH",
    "BI",
    "BJ",
    "BL",
    "BM",
    "BN",
    "BO",
    "BQ",
    "BR",
    "BS",
    "BT",
    "BV",
    "BW",
    "BY",
    "BZ",
    "CA",
    "CC",
    "CD",
    "CF",
    "CG",
    "CH",
    "CI",
    "CK",
    "CL",
    "CM",
    "CN",
    "CO",
    "CR",
    "CU",
    "CV",
    "CW",
    "CX",
    "CY",
    "CZ",
    "DE",
    "DJ",
    "DK",
    "DM",
    "DO",
    "DZ",
    "EC",
    "EE",
    "EG",
    "EH",
    "ER",
    "ES",
    "ET",
    "FI",
    "FJ",
    "FK",
    "FM",
    "FO",
    "FR",
    "GA",
    "GB",
    "GD",
    "GE",
    "GF",
    "GG",
    "GH",
    "GI",
    "GL",
    "GM",
    "GN",
    "GP",
    "GQ",
    "GR",
    "GS",
    "GT",
    "GU",
    "GW",
    "GY",
    "HK",
    "HM",
    "HN",
    "HR",
    "HT",
    "HU",
    "ID",
    "IE",
    "IL",
    "IM",
    "IN",
    "IO",
    "IQ",
    "IR",
    "IS",
    "IT",
    "JE",
    "JM",
    "JO",
    "JP",
    "KE",
    "KG",
    "KH",
    "KI",
    "KM",
    "KN",
    "KP",
    "KR",
    "KW",
    "KY",
    "KZ",
    "LA",
    "LB",
    "LC",
    "LI",
    "LK",
    "LR",
    "LS",
    "LT",
    "LU",
    "LV",
    "LY",
    "MA",
    "MC",
    "MD",
    "ME",
    "MF",
    "MG",
    "MH",
    "MK",
    "ML",
    "MM",
    "MN",
    "MO",
    "MP",
    "MQ",
    "MR",
    "MS",
    "MT",
    "MU",
    "MV",
    "MW",
    "MX",
    "MY",
    "MZ",
    "NA",
    "NC",
    "NE",
    "NF",
    "NG",
    "NI",
    "NL",
    "NO",
    "NP",
    "NR",
    "NU",
    "NZ",
    "OM",
    "PA",
    "PE",
    "PF",
    "PG",
    "PH",
    "PK",
    "PL",
    "PM",
    "PN",
    "PR",
    "PS",
    "PT",
    "PW",
    "PY",
    "QA",
    "RE",
    "RO",
    "RS",
    "RU",
    "RW",
    "SA",
    "SB",
    "SC",
    "SD",
    "SE",
    "SG",
    "SH",
    "SI",
    "SJ",
    "SK",
    "SL",
    "SM",
    "SN",
    "SO",
    "SR",
    "SS",
    "ST",
    "SV",
    "SX",
    "SY",
    "SZ",
    "TC",
    "TD",
    "TF",
    "TG",
    "TH",
    "TJ",
    "TK",
    "TL",
    "TM",
    "TN",
    "TO",
    "TR",
    "TT",
    "TV",
    "TW",
    "TZ",
    "UA",
    "UG",
    "UM",
    "US",
    "UY",
    "UZ",
    "VA",
    "VC",
    "VE",
    "VG",
    "VI",
    "VN",
    "VU",
    "WF",
    "WS",
    "YE",
    "YT",
    "ZA",
    "ZM",
    "ZW",
}

ACTIVE_CURRENCIES = {
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BHD",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BRL",
    "BSD",
    "BTN",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHF",
    "CLP",
    "CNY",
    "COP",
    "CRC",
    "CUC",
    "CUP",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ERN",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "GBP",
    "GEL",
    "GHS",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HRK",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "IQD",
    "IRR",
    "ISK",
    "JMD",
    "JOD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KPW",
    "KRW",
    "KWD",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "LYD",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MRU",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "OMR",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SDG",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SLL",
    "SOS",
    "SRD",
    "SSP",
    "STN",
    "SVC",
    "SYP",
    "SZL",
    "THB",
    "TJS",
    "TMT",
    "TND",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "USD",
    "UYU",
    "UZS",
    "VED",
    "VES",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XCD",
    "XOF",
    "XPF",
    "YER",
    "ZAR",
    "ZMW",
    "ZWL",
}

LANGUAGES = {
    "af",
    "ar",
    "bg",
    "bn",
    "bs",
    "ca",
    "cs",
    "cy",
    "da",
    "de",
    "el",
    "en",
    "en-GB",
    "eo",
    "es",
    "es-419",
    "et",
    "eu",
    "fa",
    "fi",
    "fr",
    "fy",
    "gl",
    "gsw",
    "he",
    "hi",
    "hr",
    "hu",
    "hy",
    "id",
    "is",
    "it",
    "ja",
    "ka",
    "ko",
    "lb",
    "lt",
    "lv",
    "ml",
    "nb",
    "nl",
    "nn",
    "pl",
    "pt",
    "pt-BR",
    "ro",
    "ru",
    "sk",
    "sl",
    "sr",
    "sr-Latn",
    "sv",
    "ta",
    "te",
    "th",
    "tr",
    "uk",
    "ur",
    "vi",
    "zh-Hans",
    "zh-Hant",
}


def make_script_schema(
    schema: Mapping[Any, Any], default_script_mode: str, extra: int = vol.PREVENT_EXTRA
) -> vol.Schema:
    """Make a schema for a component that uses the script helper."""
    return vol.Schema(
        {
            **schema,
            vol.Optional(CONF_MODE, default=default_script_mode): vol.In(
                SCRIPT_MODE_CHOICES
            ),
            vol.Optional(CONF_MAX, default=DEFAULT_MAX): vol.All(
                vol.Coerce(int), vol.Range(min=2)
            ),
        },
        extra=extra,
    )
