from .condition import ConditionComponent
from .foreach import ForEachComponent
from .switch import SwitchComponent

COMMON_COMPONENTS = {
    'If': ConditionComponent,
    'ForEach': ForEachComponent,
    'Switch': SwitchComponent,
}
