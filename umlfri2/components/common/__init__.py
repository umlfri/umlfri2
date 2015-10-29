from .condition import ConditionComponent
from .foreach import ForEachComponent
from .switch import SwitchComponent, SwitchCaseComponent, SwitchDefaultComponent

COMMON_COMPONENTS = {
    'If': ConditionComponent,
    'ForEach': ForEachComponent,
    'Switch': SwitchComponent,
}

SWITCH_COMPONENTS = {
    'Case': SwitchCaseComponent,
    'Default': SwitchDefaultComponent,
}
