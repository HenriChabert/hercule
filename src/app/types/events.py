from typing import Literal, NotRequired, TypeAlias, TypedDict

EventType: TypeAlias = Literal['page_opened', 'button_clicked', 'manual_trigger_in_popup']

# Page Opened

class PageOpenedEventContext(TypedDict):
  html_content: NotRequired[str]
  url: NotRequired[str]

class PageOpenedEvent(TypedDict):
  type: Literal['page_opened']
  context: PageOpenedEventContext

# Manual Trigger In Popup

class ManualTriggerInPopupEventContext(TypedDict):
  trigger_id: str
  html_content: NotRequired[str]
  url: NotRequired[str]

class ManualTriggerInPopupEvent(TypedDict):
  type: Literal['manual_trigger_in_popup']
  context: ManualTriggerInPopupEventContext


# Button Clicked

class ButtonClickedEventContext(TypedDict):
  trigger_id: str
  html_content: NotRequired[str]
  url: NotRequired[str]

class ButtonClickedEvent(TypedDict):
  type: Literal['button_clicked']
  context: ButtonClickedEventContext

EventContext: TypeAlias = PageOpenedEventContext | ButtonClickedEventContext | ManualTriggerInPopupEventContext
Event: TypeAlias = PageOpenedEvent | ButtonClickedEvent | ManualTriggerInPopupEvent