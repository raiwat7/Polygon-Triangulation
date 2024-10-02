# Introduction
This repository presents the python implementation of computational geometry algorithms to solve the Art-Gallery Problem. The main objective is to analyze the algorithms for constructing a simple polygon, obtaining monotone partitions, and performing triangulation. We then explore the application of the triangulated polygon in the context of the Art-Gallery Problem, determining the minimum number of guards necessary to cover the polygon, using graph-theoretic coloring methods.
# Executing Code
You will have to create a main.py file, and import the necessary modules to run the code. The main.py file should contain the following function calls in the order given:
## Constructing a Simple Polygon
If you already have a simple polygon, ready with known coordinates, you can call:
```python 
    polygon = DCEL(
        vertices=[
            Vertex(Point(6.65, 5.08)),
            Vertex(Point(4.74, 5.45)),
            Vertex(Point(4.8, 7)),
            Vertex(Point(3.2, 8.2)),
            Vertex(Point(4.2, 5)),
        ]
    )
```
If you do not have a polygon in mind and want to randomly generate one of n vertices, you can call:
```python
    polygon = DCEL(n)
```
## Dividing the Polygon into Monotone Pieces
To divide the polygon into monotone pieces, you can call:
```python
    monotone_partitioner = MonotonePartitioner(polygon)
    monotone_partitioner.perform_sweep_line_partition()
```
## Triangulating Each Monotone Piece
To triangulate each monotone polygon, and thereby triangulating the entire polygon, you can call:
```python
    monotone_triangulation = MonotoneTriangulation(polygon)
    monotone_triangulation.triangulate()
```
## Constructing the Dual Graph
To construct the dual graph of the triangulated polygon, you can call:
```python
    dual_graph = DualGraph(polygon)
    dual_graph.build_dual_graph()
```
## Three Coloring the Dual Graph
To three-color the dual graph, you can call:
```python
    dual_graph.three_coloring()
```
# Displaying the Results
To display the newly constructed polygon, you can call:
```python
    polygon.plot_dcel_polygon()
```
To display t partitioning of the polygon into monotone pieces, you can call:
```python
    monotone_partitioner.dcel.plot_dcel_polygon()
```
To display the triangulated polygon, you can call:
```python
    monotone_triangulation.dcel.plot_dcel_polygon()
```
To display the dual graph, you can call:
```python
    dual_graph.plot_dual_graph()
```
To display the three-colored dual graph, you can call:
```python
    dual_graph.plot_colored_dcel() # Any one of these is fine
    dual_graph.plot_colored_dcel_with_dual_graph()
```
To convert the entire polygon triangulation in a mp4 video, you can call:
```python
    polygon.animate_complete_triangulation()
```
You can find the same in the main.py file in the repository.