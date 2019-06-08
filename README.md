## Chromatic Graph Theory project - fold graph coloring

This project was an assignment from Chromatic Graph Theory course, held at the [Faculty of Mathematics and Information Science](https://ww4.mini.pw.edu.pl/) of Warsaw University of Technology. Its purpose was to investiage possible approximation algorithms to apply for a problem of multifold coloring.

To optimize the performance, Graph structure implements a different from classic (adjacency matrix/list of adjacency) approach: edges are stored as a set of neighbors for each vertex.

There were three algorithms proposed:
* modified AMIS (approximate maximum independent set) to vary independent sets based on the previously selected independent sets
* modified DSATUR (saturation was interpreted either as a number of colors of neighbors/a number of so-far-assigned colors of a vertex and colors of neighbors)
* modified CS (Connected Sequential algorithm with vertex interchange before reaching for a new color)

Results of a research were given in the report (Polish version only)
