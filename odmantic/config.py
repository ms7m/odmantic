from typing import Any, Dict, Optional, Type

from pydantic.main import BaseConfig
from pydantic.typing import AnyCallable

from odmantic.bson import BSON_TYPES_ENCODERS
from odmantic.utils import is_dunder


class BaseODMConfig:
    """Base class of the Config defined in the Models"""

    collection: Optional[str] = None

    # Inherited from pydantic
    title: Optional[str] = None
    json_encoders: Dict[Type[Any], AnyCallable] = {}


ALLOWED_CONFIG_OPTIONS = {name for name in dir(BaseODMConfig) if not is_dunder(name)}


class EnforcedPydanticConfig:
    """Configuration options enforced to work with Models"""

    validate_all = True
    validate_assignment = True


def validate_config(
    cls_config: Type[BaseODMConfig], cls_name: str
) -> Type[BaseODMConfig]:
    """Validate and build the model configuration"""
    for name in dir(cls_config):
        if not is_dunder(name) and name not in ALLOWED_CONFIG_OPTIONS:
            raise ValueError(f"'{cls_name}': 'Config.{name}' is not supported")

    if cls_config is BaseODMConfig:
        bases = (EnforcedPydanticConfig, BaseODMConfig, BaseConfig)
    else:
        bases = (
            EnforcedPydanticConfig,
            cls_config,
            BaseODMConfig,
            BaseConfig,
        )  # type:ignore

    # Merge json_encoders to preserve bson type encoders
    namespace = {
        "json_encoders": {
            **BSON_TYPES_ENCODERS,
            **getattr(cls_config, "json_encoders", {}),
        }
    }
    return type("Config", bases, namespace)
