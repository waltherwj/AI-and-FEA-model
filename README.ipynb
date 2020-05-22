# FEA and AI project

## Introduction

This project has as objectives to 

1.  Implement a model of a tetrahedral element with many more degrees of freedom than a usual one, and create a dataset of load cases and solutions

2. With this model, train a neural network that emulates the model

3. Use the trained neural network to create a new element

### How?

* Feed inputs and geometry, target is displacement field > learns mapping to displacement field 
  * This step is only done so that it can learn how to map inputs to displacement and not be reliant on a third party model to generate a displacement field. The end goal is to have the displacement field be directly fed into the network experimentally.
* Feed displacement field into another neural network, which learns a mapping from that into a simplified stress and strain output at selected nodes, in essence creating a super-element if the displacement field step, which is intermediary, is not considered. This can in theory be obtained by [digital image correlation](https://en.wikipedia.org/wiki/Digital_image_correlation_and_tracking) however deciding about this is something for the future still
  * Alternatively, with a network that is able to predict a displacement field directly from inputs, we can go back to engineering principles and calculates stresses and strains from that. This would reintroduce a lot of assumptions, however it might be worth it in terms of computation

### Bonus Objectives

1. Have the network itself impose new conditions on the model in an adversarial  way to ensure robustness

## Past Progress
#### _Implementing a 2d model for proof of concept_
  * Created script for generating correct geometry inside of SpaceClaim
  * Created script for calling geometry script from Workbench
  * Create script for generating mesh in Mechanical
  * Create script for generating model inside of Workbench
## Current Work
#### _Implementing a 2d model for proof of concept_

##### Tasks

* Automate Geometry and Mesh Generation Step
  * Create script for applying forces to element
  * Create script for saving the geometry and mesh



## Element Shape, Force & Nodal Displacement Generation Justification

#### *Element Shape*

Triangular shapes  have an advantage in relation to quadrilaterals in that it is easier to adapt them to any boundary shape. On the other hand, quadrilaterals  tend to exhibit better approximation characteristics than triangles. By creating triangular elements with the deep learning model comprised of mostly quadrilateral internal elements, the objective is that the model is able to acquire the better approximation characteristics of quadrilaterals while using triangular elements.

#### *Forces*

Forces and moments can be applied to any body (field load), edge (distributed load), or node (point load) of a finite element model. The idea is to try an approach where all of the types are present at first. This might make the model too complex for the computational resources I have access to, so if need be body forces will be disregarded for a while to make proof of concept quicker.

#### *Nodal Displacement*

In an usual FEA method the nodal displacements and the interpolation within the element is given by :
$$
\{u\}_e = [N]_e\{\Delta\}_e
$$
Where  u, N and Delta are displacement within the element, shape function and displacement at the nodes, respectively, and N is of a definite shape defined by the type of element and number of nodes.  

On the other hand, Delta is given by the boundary conditions and the equilibrium equation of the element using the stiffness matrix K, with the equation:
$$
[K]\{\Delta\} = \{F^L\}
$$
Where F is the reactions (actions to be more precise, as it is the negative of the actual reactions) at the nodes. 

The goal is thus that, given a set of boundary conditions and forces along the entire element, the model directly learns a certain equivalent mapping M that that maps into the displacement field within the entire element. 
$$
M: (F_e,  \Delta_{BC})  \mapsto u_e
$$
Therefore the element has to be generated with arbitrary nodal displacements to train the model.



## Relevant Links

[How to execute APDL commands from python session](https://www.youtube.com/watch?v=bSP9pi-4QW0)

[Use a Named Selection as Scoping of a Load or Support](https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v201/en/act_script/act_script_examples_NamedSelection_as_Scoping.html)

[Export Result Object to STL](https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v201/en/act_script/act_script_examples_export_result_object.html) *CAN ONLY ACCES ANSYS SCRIPTING GUIDE THROUGH INSIDE OF MECHANICAL > USE SEARCH FUNCTIONS "SCRIPTING"*

[Using IronPython/ACT console](https://www.youtube.com/watch?v=txPimWRh8nM) 

[Creating XML and Python in Ansys](https://www.youtube.com/watch?v=fURQ-22YKmc)

[ANSYS scripting examples](https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v201/en/act_script/pt03.html) *CAN ONLY ACCES ANSYS SCRIPTING GUIDE THROUGH INSIDE OF MECHANICAL > USE SEARCH FUNCTIONS "SCRIPTING"*