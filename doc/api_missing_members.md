Missing API members
===================

interface Solution
------------------
- save()
- saveAs(fileName: string)
- createProject(template: ProjectTemplate)

interface ElementObject
-----------------------
- connectWith(other: ElementObject, connectionType: ConnectionType): ConnectionObject
- createChild(elementType: ElementType): ElementObject
- createDiagram(diagramType: DiagramType): Diagram
- getConnectionTo(other: ElementObject): ConnectionObject

interface Diagram
-----------------
- showElement(element: ElementObject): ElementVisual
- showConnection(connection: ConnectionObject): ConnectionVisual
- getElementVisualAt(position: xy): ElementVisual
- getElementVisualIn(area: xywh): ElementVisual[]
- values[] setter
- select(item: Visual) // might be implemented as new Selection interface

interface ConnectionObject
--------------------------
- getConnectedElement(other: ElementObject): ElementObject

interface FileType
------------------
_File types will be registered in a config file_
_Entirely new interface_
- id: string
- exportEnabled: boolean
- importEnabled: boolean
- event export(fileName: string)
- event import(fileName: string)

interface ProjectTemplate
-------------------------
_Entirely new interface_
- metamodelIdentifier: string
- name: string

interface Application
---------------------
- templates: ProjectTemplate[]
- load(fileName: string)
- createSolution(template: ProjectTemplate)
- createEmptySolution()
