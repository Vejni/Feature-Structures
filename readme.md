# A Mathematical Model of Conceptual Blending
## A Step Towards a Computational Implementation

This repository contains code written for the master's thesis entitled A Mathematical Model of Conceptual Blending. The project has been written and tested in Python 3.10.0. All requirements can be found in the requirements.txt file. 

### Abstract

Conceptual blending is an extensively studied theory in cognitive science, referring to the cognitive process of
combining separate pieces of knowledge to create new meaning. Because of the key role the theory plays in day-to-
day thought and language, it has been adopted in the field of computational creativity, for guiding creative systems
to create novel concepts. This adoption has led to many algorithmic formalisations of conceptual blending and
information integration, each with their unique set of assumptions and applications. The lack of mathematical
foundation of the conceptual blending theory made these implementations even harder to compare, which is why
a representation-free formalisation of the theory was needed. Such a framework has recently been proposed
by Schorlemmer and Plaza, describing the conceptual blending theory through category theoretic constructions,
obtaining a mathematical model that is uniform across different representation formalisms.

This thesis aims to build upon the mathematical model of Schorlemmer and Plaza, with the overall goal
of a computational description of the theory. To achieve this, several notions of the uniform model are refined
and formalised in a way that is compatible with an algorithmic implementation. We also expand the theory by
formalising some governing principles, discussing their relevance in achieving cognitively useful blends. We offer
an algorithmic implementation for two specific representations, typed feature structures and CASL Specifications,
which are presented before the uniform model. Lastly, we present an application of our framework in the theory
of sense-making of diagrams, arguing for its aptness in describing the cognitive process of conceptual blending.
The theory and implementation of this thesis can be used as a template for adopting different representation
formalisms, offering suitable foundations of future algorithmic developments.

### Project Structure

* Root: The root folder contains project speficic files, and also the amalgam.py script, which contains the category theoretic, higher-level code as methods to the abstract class Category. Implementations of representation formalisms should inherit from this class, providing the abstract methods.
* Feature Structures: Contains code and output plots for the representation formalism of typed feature structures. To generate amalgams for feature structures, one should run the feature_structure_category.py script.
* CASL Specifications: Contains CASL scripts, and Python code for implementing the conceptual blending of CASL theories. To generate amalgams for CASL scripts, the ones in the specs folder, one should run the casl_specifications_category.py script.

### Further Work

In order to implement other representation formalisms, it is suggested to create a separate folder, and two scripts similarly to CASL Specifications and Feature Structures. On script should define the subclass of the class Category, and implement the abstract methods according to their interfacing requirements. The details of these implementation could be put in the second script, to encapsulate the computations. The methods that need implementing are denoted with the @abc.abstractmethod class modifiers. Similarly as above, this new script should be run instead of amalgam.py.

