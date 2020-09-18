from dataclasses import dataclass
from data_utils.fields import Field
from data_utils.field_validators import is_order_side, is_order_state


@dataclass
class Order:
    side: str = Field(str, validators=[is_order_side])
    symbol_name: str = Field(str)
    price: float = Field(float)
    state: str = Field(str, validators=[is_order_state], default='COMMITTED')
