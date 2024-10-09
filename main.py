from DualGraph import DualGraph
from MonotonePartitioner import MonotonePartitioner
from MonotoneTriangulation import MonotoneTriangulation
from elements.DCEL import DCEL
from elements.Point import Point
from elements.Vertex import Vertex


def triangulate_and_animate(polygon):
    polygon.plot_dcel_polygon()

    monotone_partitioner = MonotonePartitioner(polygon)
    monotone_partitioner.perform_sweep_line_partition()
    polygon.plot_dcel_polygon()

    monotone_triangulation = MonotoneTriangulation(polygon)
    monotone_triangulation.triangulate()
    polygon.plot_dcel_polygon()

    dual_graph = DualGraph(polygon)
    dual_graph.build_dual_graph()
    dual_graph.plot_dual_graph()

    dual_graph.three_coloring()
    dual_graph.plot_dcel_and_dual_graph()
    dual_graph.plot_colored_dcel_with_dual_graph()

    polygon.animate_complete_triangulation()

def polygon_with_34_vertices():
    polygon = DCEL(
        vertices=[
            Vertex(Point(10.07, 10)),  # Starting at the top
            Vertex(Point(6.98, 9.51)),
            Vertex(Point(10, 7)),
            Vertex(Point(8.69, 5.52)),
            Vertex(Point(8.4, 6.4)),
            Vertex(Point(8.2, 7.8)),
            Vertex(Point(6.27, 7.36)),
            Vertex(Point(7.07, 6.54)),
            Vertex(Point(6.65, 5.08)),
            Vertex(Point(4.74, 5.45)),
            Vertex(Point(4.8, 7)),
            Vertex(Point(3.2, 8.2)),
            Vertex(Point(4.2, 5)),
            Vertex(Point(3.43, 6.29)),
            Vertex(Point(1.8, 4.6)),
            Vertex(Point(3.2, 5.4)),
            Vertex(Point(2.1, 3.1)),
            Vertex(Point(3.38, 3.53)),
            Vertex(Point(2.8, 2.4)),
            Vertex(Point(5.21, 2.72)),
            Vertex(Point(6.41, 3.92)),
            Vertex(Point(6.5, 1.14)),
            Vertex(Point(8.8, 2.4)),
            Vertex(Point(8.75, 1.26)),
            Vertex(Point(12.07, 1.4)),
            Vertex(Point(15, 4.8)),
            Vertex(Point(15.47, 7.3)),
            Vertex(Point(14.82, 8.71)),
            Vertex(Point(13.22, 8.74)),
            Vertex(Point(14.6, 6.4)),
            Vertex(Point(12.6, 2.6)),
            Vertex(Point(11.85, 5.24)),
            Vertex(Point(7.37, 2.29)),
            Vertex(Point(11.54, 6.96)),
        ]
    )
    triangulate_and_animate(polygon)

def polygon_with_15_vertices():
    polygon_example_book = DCEL(
        vertices=[Vertex(Point(47, 172)), Vertex(Point(18, 152)), Vertex(Point(39 , 127)), Vertex(Point(16, 113)), Vertex(Point(34, 99)), Vertex(Point(7, 68)),
                  Vertex(Point(29, 42)), Vertex(Point(60, 54)), Vertex(Point(94, 5)), Vertex(Point(86, 78)), Vertex(Point(120, 65)), Vertex(Point(153, 128)),
                  Vertex(Point(107, 109)), Vertex(Point(94, 168)), Vertex(Point(70, 158))])

    triangulate_and_animate(polygon_example_book)

def generate_and_triangulate_random_polygon(n):
    # Random Polygon Generation
    polygon_example = DCEL(n)
    polygon_example.plot_dcel()
    polygon_example.display_dcel()
    triangulate_and_animate(polygon_example)

def main():
    polygon_with_34_vertices()

if __name__ == "__main__":
    main()