from typing import Literal, TypeAlias, TypedDict

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

# Inject Script

class InjectScriptActionParams(TypedDict):
  script: str

class InjectScriptAction(TypedDict):
  type: Literal['inject_script']
  params: InjectScriptActionParams

Action: TypeAlias = ShowAlertAction | ShowConsoleAction | InjectScriptAction