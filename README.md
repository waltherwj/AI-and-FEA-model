# FEA and AI project

## Introduction

This project has as objectives to 

**1** - Implement a model of a tetrahedral element with many more degrees of freedom than a usual one, and create a dataset of load cases and solutions

**2** - With this model, train a neural network that emulates the model

**3** - Use the trained neural network to create a new element

### How?

* Feed inputs and geometry, target is displacement field > learns mapping to displacement field 
  * This step is only done so that it can learn how to map inputs to displacement and not be reliant on a third party model to generate a displacement field. The end goal is to have the displacement field be directly fed into the network experimentally.
* Feed displacement field into another neural network, which learns a mapping from that into a simplified stress and strain output at selected nodes, in essence creating a super-element if the displacement field step, which is intermediary, is not considered.

### Bonus Objectives

**1** - Have the network itself impose new conditions on the model in an adversarial  way to ensure robustness

## Past Progress

## Current Work
Implementing a 2d model for proof of concept



## Relevant Links

https://www.youtube.com/watch?v=bSP9pi-4QW0

https://www.youtube.com/watch?v=WCsvagzvAv4

https://www.youtube.com/watch?v=fOOC8XXxsKc

https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v201/en/act_script/pt03.html