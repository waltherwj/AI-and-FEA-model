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
  * Create script for generating correct geometry inside of SpaceClaim
## Current Work
#### _Implementing a 2d model for proof of concept_

##### Tasks

* Automate Geometry and Mesh Generation Step

  * Create script for generating model inside of Workbench
  * Create script for calling the geometry-generating script
  * Create script for saving the geometry and mesh





## Relevant Links

https://www.youtube.com/watch?v=bSP9pi-4QW0

https://www.youtube.com/watch?v=WCsvagzvAv4

https://www.youtube.com/watch?v=fOOC8XXxsKc

https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v201/en/act_script/pt03.html