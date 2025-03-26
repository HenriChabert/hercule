from typing import Literal, NotRequired, TypeAlias, TypedDict

# Show Alert


class ShowAlertActionParams(TypedDict):
    message: str


class ShowAlertAction(TypedDict):
    type: Literal["show_alert"]
    params: ShowAlertActionParams


# Show Console


class ShowConsoleActionParams(TypedDict):
    message: str


class ShowConsoleAction(TypedDict):
    type: Literal["show_console"]
    params: ShowConsoleActionParams


# Inject Script


class InjectScriptActionParams(TypedDict):
    script: str


class InjectScriptAction(TypedDict):
    type: Literal["inject_script"]
    params: InjectScriptActionParams


# Insert Button


class ButtonParams(TypedDict):
    id: str
    label: str
    variant: Literal["primary", "secondary", "success", "danger", "warning"]
    size: Literal["small", "medium", "large"]
    position: Literal[
        "top-right", "top-left", "bottom-right", "bottom-left", "in-content"
    ]
    anchorCssSelector: NotRequired[str]
    positionToAnchor: NotRequired[
        Literal["first-child", "last-child", "nth-child", "before", "after", "replace"]
    ]
    nthChildIndex: NotRequired[int]
    applyOnAllCssSelectorMatches: NotRequired[bool]
    customHtml: NotRequired[str]
    customCss: NotRequired[str]
    anchorCustomCss: NotRequired[str]


class InsertButtonActionParams(TypedDict):
    button: ButtonParams
    buttonAction: Literal["launch_trigger"]
    triggerId: NotRequired[str]


class InsertButtonAction(TypedDict):
    type: Literal["insert_button"]
    params: InsertButtonActionParams


Action: TypeAlias = (
    ShowAlertAction | ShowConsoleAction | InjectScriptAction | InsertButtonAction
)
