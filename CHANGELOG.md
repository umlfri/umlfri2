Changelog
=========

All notable changes to this project will be documented in this file.

[2.2.1] 2020-09-16
------------------

### User changes
- support for HiDPI monitors

### Fixes
- property dialog validation when tabs are changed using a mouse wheel or ctrl+tab (issue #5)
- show save dialog on save action, if parent directory of the project no longer exists (issue #6)
- fixed exception on switching application tab while doing an action on a diagram (issue #7)
- macMint icon theme available again (issue #9)
- open project tabs when solution is opened by passing command line argument (issue #13)
- EditorWidget's timerEvent replaced by QTimer to prevent unexpected timer firing (issue #14)
- Control unicode characters removed from strings when saving project, (issue #8)

[2.2.0] 2019-09-05
------------------

### User changes
- context help buttons removed from dialog windows, as it was not functional
- toolbox size can be reduced by user
- closing properties dialog when some data was modified causes showing the confirmation dialog (issue #4)
- possibility to move items up/down in lists in properties dialog
- errors in UML .FRI are reported to developers using sentry.io
- top-right-side icon for selected element to simplify drawing connections
- current diagram action can be canceled using esc key
- full screen mode can be closed using gui button too
- export/copy as image dialog options are saed to the application config file

### UML changes
- double french-quotes in attribute stereotype fixed

### Power user changes
- binary Windows version uses Python 3.7

### Metamodel changes
- support for ufl macros with lambda function argument
- generic types support for ufl macros
- new built-in macros for use in ufl expressions:
    - `iter->all(...)`
    - `iter->any(...)`
    - `iter->order_by(...)`
    - `iter->reduce(...)`
    - `iter->select(...)`
    - `iter->where()`
    - `nullable->default(...)`
    - `nullable->iterate()`
    - `str->empty()`
    - `str->has_text()`
- automatic ufl expression casts to boolean are disabled as they no longer needed
- dot (`.`) operator for nullables and iterables in ufl expressions
- better support for nullables in metamodel

### Plugin API changes

- exceptions are supported in public api
- PartNotFound exception is rised from public api metamodel part getters, when the part is not found

### Fixes
- new version notification is no longer showed twice
- qt version for about dialog is detected at runtime
- decimal literals are correctly handled in ufl expressions
- python builtins disabled when compiling ufl expression
- correct error report for errors in ufl expressions
- logical operators can be written using textual representation (gt, lt, ge, le, eq, ne, and, or) to make it easier to be written in xml
- copying transparent images to clipboard works in most applications on windows too
- fixed problem with duplicating elements in the same diagram (issue #3)
- correct behavior of element resizing when the mouse cursor is moved out of diagram
- resize element action is no longer added to undo menu, when resize operation was started by a user but element was not really resized
- fixed incompatibilities for python 3.7
- element is correctly removed from selection, when it is removed from associated diagram
- full screen window is no longer closed randomly
- dont try to open full screen window when alt-enter is pressed on a start page

[2.1.1] 2019-02-25
------------------

### Fixes
- fixed problem with missing DLLs on Windows 7 installation

[2.1.0] 2018-09-13
------------------

### User changes
- context menu for recent files on the start page
- recent files can be pinned on the startpage
- new application settings dialog
- new updates are being notified to user at the application startup
- fonts are rendered with antialiasing in diagrams
- menu items rearanged a bit
- text hyperlinks in the about dialog contains tooltip with the destination url
- nicer rendering of metamodel description in the new project dialog
- diagram printing
- select all characters in a first textbox after save in a properties dialog
- simpler element addition from the project tree context menu
- fullscreen can be closed by the alt-enter shortcut
- fullscreen diagram takes bigger proportion of the screen
- tabs can be closed by middle click
- possibility to lock tab
- online addon installation and updates directly from the UML .FRI gui
- addons cannot be installed from a file
- addons installed from the gui can be uninstalled too
- nicer layout for simple property dialog without tabs
- metamodel config dialog
- checking for value changes on tab switch in the properties dialog is more
  user friendly

### UML changes
- new object diagram in UML addon
- package element has been tided up a bit
- testing use case diagram removed from the infjavauml metamodel

### Power user changes
- recent files config format has been changed
- frip2 file contains mimetype identifier and save version as a plaintext files
- moved to VisualStudio 2017 on the Windows platform

### Metamodel changes
- project templates can have name translated in a metamodel definition
- support for true/false/null literals in ufl expressions
- new format for project templates in a metamodel
- diagrams can be marked as opened or even locked in a project template
- new variable metadata access operator in ufl expressions
- item name in the ForEach component is mandatory
- index attribute for ForEach component is not allowed anymore, use metadata
  access operator instead
- new object metadata access operator in ufl expressions
- logical and arithmetic operators in ufl expressions
- support for if-then-else component
- new iterator access operator
- Table component is checked for having only rows or only columns defined
  as its children
- more ufl types (int, decimal) are supported by properties dialog
- metamodel can contain as many definition files as needed
- new ufl macro system, macros cannot be defined by a metamodel creator for now
- Color and Font enums available in ufl expressions, their items have color
  type and font type respectively
- division by zero yields inf/nan in ufl expression
- better type checking on ufl expression return value
- non-expanded box children are non-resizable by default
- lambda expression support in ufl expression

### Plugin API changes
- nicer documentation formatting
- AddonStarter renamed to PluginStarter as it is not needed to start all addon
  types

### Fixes
- toolbox is disabled on start page
- selected connection takes preference when performing mouse actions on
  drawing area (even if it is not on top of all other objects)
- toolbox widget is working properly on mac os
- fixed problems with incorrect detection of changes on elements/connections/
  diagrams when edited by a user
- fixed problem with doubleclicking on the zoomed diagram (issue #1)
- painting zoomed diagram is not leaving artifacts at the diagram sides
- instructions to install UML .FRI on mac have been updated
- same element (identity) connections fixed (i.e. issue #2)
- redraw element visual representation when the child node was changed if
  needed (for example for packages)
- non resizable element is resized to a minimum size, when its properties
  are changed
- fixed arrow and rectangle rounds rotations in element/connection rendering
- fixed sub-diagram menu on a element
- correct resizing of non-resizable elements
- recent files config encoding set to utf-8 to enable unicode file paths
- Line component detects correctly its orientation if no orientation is given
  explicitly
- Boolean constants in metamodel has to be defined by true/false keywords only
- Removed circular cache dependency in the ElementVisual class
- Fixed problems with toolbox rendering on Mac Os X platform
- All types with the exception of image type can be included in a snippet
- Metamodel version is being checked on project loading
- Incorrect element/connection/diagram attributes in a project file are ignored
  on a project load
- Fixed editing/loading/saving ulf list type with immutable item type
- fixed problems with adding existing ufl object to the list (i.e. by
  undo/redo)
- inverting a color works correctly
- Color's attributes (r, g, b, and a) are accessible for color type only
- fixed incorrect parsing of rgb color string
- fixed HBox and VBox children size computation when one or more children are
  marked as expanded
- fixed exception on closing properties dialog opened from properties widget

[2.0.0] 2017-09-12
------------------

First public release
