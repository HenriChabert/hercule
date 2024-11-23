from typing import Literal, TypedDict, TypeAlias

ActionType: TypeAlias = Literal['show_alert']

# Show Alert

class ShowAlertActionParams(TypedDict):
  message: str

class ShowAlertAction(TypedDict):
  type: Literal['show_alert']
  params: ShowAlertActionParams

# Show Console

class ShowConsoleActionParams(TypedDict):
  message: str

class ShowConsoleAction(TypedDict):
  type: Literal['show_console']
  params: ShowConsoleActionParams

Action: TypeAlias = ShowAlertAction | ShowConsoleAction