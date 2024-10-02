from DualGraph import DualGraph
from MonotonePartitioner import MonotonePartitioner
from MonotoneTriangulation import MonotoneTriangulation
from elements.DCEL import DCEL
from elements.Point import Point
from elements.Vertex import Vertex


def main():
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
    dual_graph.plot_colored_dcel_with_dual_graph()

    polygon.animate_complete_triangulation()

if __name__ == "__main__":
    main()