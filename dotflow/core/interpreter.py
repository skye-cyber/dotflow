"""
Main interpreter class that orchestrates all functionality.
"""

from typing import Dict, List, Optional, Any
from contextlib import contextmanager

from .models import (
    Node,
    Edge,
    Cluster,
    NodeShape,
    EdgeStyle,
    EdgeStyleConfig,
    Direction,
)
from .themes import Theme, ThemeManager
from ..utils.validators import validate_node_id, validate_label
from ..utils.exceptions import (
    NodeNotFoundError,
)
from ..core.models import NodeStyle


class DotInterpreter:
    """
    Main interpreter for creating DOT diagrams with multiple API styles.
    """

    def __init__(
        self,
        name: str = "flow",
        theme: Theme = Theme.DEFAULT,
        direction: Direction = Direction.TOP_DOWN,
    ):
        self.name = name
        self.theme = theme
        self.direction = direction
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.clusters: Dict[str, Cluster] = {}
        self._current_cluster: Optional[str] = None
        self._theme_config = ThemeManager.get_theme_config(theme)

        # Initialize default graph attributes
        self._graph_attrs = {
            "bgcolor": self._theme_config["bg_color"],
            "rankdir": direction.value,
        }

    def _create_node(
        self, node_id: str, label: str, shape: NodeShape, **kwargs
    ) -> Node:
        """Create a node with theme-appropriate styling."""
        validate_node_id(node_id)
        validate_label(label)

        # Merge theme style with any custom styles
        theme_style = self._theme_config["node_style"]
        custom_style = theme_style.__dict__.copy()
        custom_style.update(kwargs)

        style = NodeStyle(**custom_style)
        node = Node(node_id, label, shape, style)

        if self._current_cluster and self._current_cluster in self.clusters:
            self.clusters[self._current_cluster].add_node(node)
        else:
            self.nodes[node_id] = node

        return node

    def _create_edge(
        self,
        from_node: str,
        to_node: str,
        label: Optional[str] = None,
        style: EdgeStyle = EdgeStyle.SOLID,
        **kwargs,
    ) -> Edge:
        """Create an edge with theme-appropriate styling."""
        # Validate nodes exist
        if from_node not in self.nodes and not any(
            from_node in cluster.nodes for cluster in self.clusters.values()
        ):
            raise NodeNotFoundError(f"Source node '{from_node}' not found")

        if to_node not in self.nodes and not any(
            to_node in cluster.nodes for cluster in self.clusters.values()
        ):
            raise NodeNotFoundError(f"Target node '{to_node}' not found")

        if label:
            validate_label(label)

        # Merge theme style with any custom styles
        theme_style = self._theme_config["edge_style"]
        custom_style = theme_style.__dict__.copy()
        custom_style.update({"style": style, **kwargs})

        edge_style = EdgeStyleConfig(**custom_style)
        edge = Edge(from_node, to_node, label, edge_style)

        if self._current_cluster and self._current_cluster in self.clusters:
            self.clusters[self._current_cluster].add_edge(edge)
        else:
            self.edges.append(edge)

        return edge

    def node(self, *args, **kwargs):
        return self._create_node(*args, **kwargs)

    def edge(self, *args, **kwargs):
        return self._create_edge(*args, **kwargs)

    # Core API methods
    def start(self, node_id: str, label: Optional[str] = None) -> "DotInterpreter":
        """Start a flow with an initial node (ellipse shape)."""
        label = label or node_id
        self._create_node(node_id, label, NodeShape.ELLIPSE)
        return self

    def process(self, node_id: str, label: Optional[str] = None) -> "DotInterpreter":
        """Create a process node (rectangle shape)."""
        label = label or node_id
        self._create_node(node_id, label, NodeShape.RECTANGLE)
        return self

    def decision(
        self, node_id: str, question: Optional[str] = None
    ) -> "DotInterpreter":
        """Create a decision node (diamond shape)."""
        label = question or node_id
        self._create_node(node_id, label, NodeShape.DIAMOND)
        return self

    def end(self, node_id: str, label: Optional[str] = None) -> "DotInterpreter":
        """Create an end node (ellipse shape)."""
        label = label or node_id
        self._create_node(
            node_id, label, NodeShape.ELLIPSE, style="filled", fillcolor="#ffcccc"
        )
        return self

    def input_output(
        self, node_id: str, label: Optional[str] = None
    ) -> "DotInterpreter":
        """Create an input/output node (parallelogram shape)."""
        label = label or node_id
        self._create_node(node_id, label, NodeShape.PARALLELOGRAM)
        return self

    def connect(
        self,
        from_node: str,
        to_node: str,
        label: Optional[str] = None,
        style: EdgeStyle = EdgeStyle.SOLID,
    ) -> "DotInterpreter":
        """Connect two nodes with an optional label."""
        self._create_edge(from_node, to_node, label, style)
        return self

    @contextmanager
    def cluster(self, name: str, label: str, **style_kwargs):
        """Context manager for creating clusters."""
        previous_cluster = self._current_cluster
        self._current_cluster = name

        cluster_style = {
            "style": "filled",
            "color": "lightgrey",
            "fillcolor": "lightgrey:white",
            "gradientangle": "90",
            **style_kwargs,
        }
        self.clusters[name] = Cluster(name, label, cluster_style)

        try:
            yield self
        finally:
            self._current_cluster = previous_cluster

    def set_graph_attr(self, key: str, value: Any):
        """Set a graph-level attribute."""
        self._graph_attrs[key] = value

    def to_dot(self) -> str:
        """Generate DOT language code."""
        lines = [f"digraph {self.name} {{"]

        # Add graph attributes
        for key, value in self._graph_attrs.items():
            lines.append(f'  {key}="{value}";')

        lines.append('  node [fontname="Arial", fontsize=12];')
        lines.append('  edge [fontname="Arial", fontsize=10];')
        lines.append("")

        # Add nodes
        for node in self.nodes.values():
            lines.append(f"  {node.to_dot()}")

        # Add edges
        for edge in self.edges:
            lines.append(f"  {edge.to_dot()}")

        # Add clusters
        for cluster in self.clusters.values():
            lines.extend([f"  {line}" for line in cluster.to_dot()])

        lines.append("}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.to_dot()


# Alias for backward compatibility
Flow = DotInterpreter
