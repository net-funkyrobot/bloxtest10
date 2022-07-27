import os


def application_id(default="e~example") -> str:
    # Fallback to example on local or if this is not specified in the
    # environment already
    result = os.environ.get("GAE_APPLICATION", default)
    return result


def is_production_environment() -> bool:
    return not is_development_environment()


def is_development_environment() -> bool:
    return "GAE_ENV" not in os.environ or os.environ["GAE_ENV"] != "standard"
