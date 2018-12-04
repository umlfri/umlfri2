Changelog
=========

All notable changes to this project will be documented in this file.

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
