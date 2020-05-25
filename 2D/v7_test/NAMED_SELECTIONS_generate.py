## Script to generate named selections for forces and displacements

nodes2 = Model.NamedSelections.Children[4]
nodes2.ScopingMethod = GeometryDefineByType.Worksheet
criterion = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion
nodes2.GenerationCriteria.Add(criterion(actionType = SelectionActionType.Add)) ##creates new selection criterion
