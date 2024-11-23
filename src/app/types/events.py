from typing import Literal, TypedDict, TypeAlias, NotRequired

EventType: TypeAlias = Literal['page_opened', 'button_clicked']

# Page Opened

class PageOpenedEventContext(TypedDict):
  url: str

class PageOpenedEvent(TypedDict):
  type: Literal['page_opened']
  context: PageOpenedEventContext

# Button Clicked

class ButtonClickedEventContext(TypedDict):
  trigger_id: str
  url: str

class ButtonClickedEvent(TypedDict):
  type: Literal['button_clicked']
  context: ButtonClickedEventContext

EventContext: TypeAlias = PageOpenedEventContext | ButtonClickedEventContext
Event: TypeAlias = PageOpenedEvent | ButtonClickedEvent