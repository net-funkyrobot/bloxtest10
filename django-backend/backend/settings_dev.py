import os

import structlog
from django_structlog.processors import inject_context_dict

from backend.settings import *  # noqa: F401, F403
from backend.settings import BASE_DIR

# CORE

DEBUG = True

MIDDLEWARE = [
    "django_structlog.middlewares.RequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Standard Django auth middleware used here
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "backend.core.middleware.TaskEnvironmentMiddleware",
]

# Use a local SQLlite database like settings_test but specify a different
# sqlite file
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# INTEGRATIONS

# Set MAILERLITE_GROUP to "testing" so test contacts don't pollute the mailing list
MAILERLITE_GROUP = "testing"


# LOGGING

_shared_processors = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.stdlib.PositionalArgumentsFormatter(),
]

_builtin_processors = [
    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    # Use console renderer for local development
    structlog.dev.ConsoleRenderer(colors=True),
]

_builtin_pre_chain = [inject_context_dict, *_shared_processors]

_structlog_processors = [
    structlog.stdlib.filter_by_level,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.UnicodeDecoder(),
    *_shared_processors,
    # Wrap for builtin logging as very last processor
    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processors": _builtin_processors,
            "foreign_pre_chain": _builtin_pre_chain,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    },
}

structlog.configure(
    processors=_structlog_processors,
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
