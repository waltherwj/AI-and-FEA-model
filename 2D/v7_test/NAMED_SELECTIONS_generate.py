## Script to generate named selections for forces and displacements

nodes2 = Model.NamedSelections.Children[4]
nodes2.ScopingMethod = GeometryDefineByType.Worksheet
criterion = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion
#Criterion Options: active: bool, actionType: SelectionActionType, 
#entityType: SelectionType, criterionType: SelectionCriterionType, 
#operatorType: SelectionOperatorType, value: object, 
#lowerBound: Quantity, upperBound: Quantity, 
#coordinateSystem: CoordinateSystem
criterion(entityType = SelectionType.MeshNode)
nodes2.GenerationCriteria[1].EntityType = SelectionType.MeshNode
nodes2.GenerationCriteria.Add(criterion(actionType = SelectionActionType.Add)) ##creates new selection criterion

