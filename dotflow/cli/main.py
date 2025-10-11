"""
Main CLI entry point for DotFlow.
"""

import click
import sys
from pathlib import Path
from typing import Optional

from ..core.interpreter import DotInterpreter
from ..core.themes import Theme
from ..core.models import Direction, NodeShape
from ..exporters.image import ImageExporter
from ..exporters.dot import DotExporter
from ..utils.exceptions import DotFlowError


@click.group()
@click.version_option()
def cli():
    """DotFlow - Python-based DOT language interpreter with multiple API styles."""
    pass


@cli.command()
@click.argument("output", type=click.Path())
@click.option("--name", "-n", default="flow", help="Name of the flow diagram")
@click.option(
    "--theme",
    "-t",
    type=click.Choice([t.value for t in Theme]),
    default="default",
    help="Color theme for the diagram",
)
@click.option(
    "--direction",
    "-d",
    type=click.Choice([d.value for d in Direction]),
    default="TB",
    help="Layout direction",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["png", "svg", "pdf", "dot"]),
    default="png",
    help="Output format",
)
@click.option("--dsl-file", "-i", type=click.File("r"), help="Input DSL file")
@click.option("--dsl-text", "-s", help="DSL text directly from command line")
def generate(
    output: str,
    name: str,
    theme: str,
    direction: str,
    format: str,
    dsl_file: Optional[click.File],
    dsl_text: Optional[str],
):
    """Generate a flow diagram from DSL input."""

    try:
        # Create interpreter
        flow = DotInterpreter(
            name=name, theme=Theme(theme), direction=Direction(direction)
        )

        # Get DSL content
        dsl_content = ""
        if dsl_file:
            dsl_content = dsl_file.read()
        elif dsl_text:
            dsl_content = dsl_text
        else:
            click.echo(
                "Error: Either --dsl-file or --dsl-text must be provided", err=True
            )
            sys.exit(1)

        # Parse DSL and generate diagram
        flow.parse_dsl(dsl_content)

        # Export based on format
        if format == "dot":
            exporter = DotExporter()
            exporter.export(flow.to_dot(), output)
        else:
            exporter = ImageExporter()
            exporter.export(flow.to_dot(), output, format)

        click.echo(f"Successfully generated {format.upper()} diagram: {output}")

    except DotFlowError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("output", type=click.Path())
@click.option("--name", "-n", default="flow", help="Name of the flow diagram")
@click.option(
    "--theme",
    "-t",
    type=click.Choice([t.value for t in Theme]),
    default="default",
    help="Color theme for the diagram",
)
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode")
def wizard(output: str, name: str, theme: str, interactive: bool):
    """Interactive wizard for creating flow diagrams."""

    try:
        flow = DotInterpreter(name=name, theme=Theme(theme))

        if interactive:
            _run_interactive_wizard(flow)
        else:
            _run_quick_wizard(flow)

        # Always generate both DOT and PNG
        dot_exporter = DotExporter()
        image_exporter = ImageExporter()

        dot_path = Path(output).with_suffix(".dot")
        png_path = Path(output).with_suffix(".png")

        dot_exporter.export(flow.to_dot(), str(dot_path))
        image_exporter.export(flow.to_dot(), str(png_path))

        click.echo(f"Successfully generated:")
        click.echo(f"  - DOT file: {dot_path}")
        click.echo(f"  - PNG file: {png_path}")

    except DotFlowError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


def _run_interactive_wizard(flow: DotInterpreter):
    """Run interactive wizard for building flows."""
    click.echo("🐍 DotFlow Interactive Wizard")
    click.echo("=" * 40)

    nodes = []
    current_node = None

    while True:
        click.echo("\nCurrent flow:")
        click.echo(flow.to_dot())
        click.echo()

        click.echo("Options:")
        click.echo("  1. Add start node")
        click.echo("  2. Add process node")
        click.echo("  3. Add decision node")
        click.echo("  4. Add end node")
        click.echo("  5. Connect nodes")
        click.echo("  6. Add cluster")
        click.echo("  7. Finish and generate")

        choice = click.prompt("Choose an option", type=int)

        if choice == 1:
            node_id = click.prompt("Enter node ID")
            flow.start(node_id)
            nodes.append(node_id)
            current_node = node_id
            click.echo(f"✓ Added start node: {node_id}")

        elif choice == 2:
            node_id = click.prompt("Enter node ID")
            label = click.prompt("Enter label (optional)", default=node_id)
            flow.process(node_id, label)
            nodes.append(node_id)
            current_node = node_id
            click.echo(f"✓ Added process node: {node_id}")

        elif choice == 3:
            node_id = click.prompt("Enter node ID")
            question = click.prompt("Enter question", default=node_id)
            flow.decision(node_id, question)
            nodes.append(node_id)
            current_node = node_id
            click.echo(f"✓ Added decision node: {node_id}")

        elif choice == 4:
            node_id = click.prompt("Enter node ID")
            flow.end(node_id)
            nodes.append(node_id)
            current_node = node_id
            click.echo(f"✓ Added end node: {node_id}")

        elif choice == 5:
            if len(nodes) < 2:
                click.echo("Need at least 2 nodes to connect")
                continue

            click.echo("Available nodes: " + ", ".join(nodes))
            from_node = click.prompt("From node", default=current_node)
            to_node = click.prompt("To node")
            label = click.prompt("Label (optional)", default="")

            if from_node not in nodes:
                click.echo(f"Node {from_node} not found")
                continue
            if to_node not in nodes:
                click.echo(f"Node {to_node} not found")
                continue

            flow.connect(from_node, to_node, label if label else None)
            click.echo(f"✓ Connected {from_node} -> {to_node}")

        elif choice == 6:
            cluster_name = click.prompt("Enter cluster name")
            cluster_label = click.prompt("Enter cluster label", default=cluster_name)

            with flow.cluster(cluster_name, cluster_label):
                click.echo(f"Now adding nodes to cluster '{cluster_name}'...")
                # For simplicity, we'll just add one node
                node_id = click.prompt("Enter node ID for cluster")
                flow.process(node_id)
                nodes.append(node_id)
                current_node = node_id

        elif choice == 7:
            break
        else:
            click.echo("Invalid option")


def _run_quick_wizard(flow: DotInterpreter):
    """Run quick wizard with predefined flow."""
    click.echo("🚀 DotFlow Quick Wizard")
    click.echo("Creating a sample workflow...")

    # Create a sample flow
    (
        flow.start("Start")
        .process("Process Data")
        .decision("Data Valid?")
        .connect("Data Valid?", "End", label="Yes")
        .connect("Data Valid?", "Process Data", label="No")
    )


@cli.command()
@click.argument("dsl_file", type=click.File("r"))
def validate(dsl_file: click.File):
    """Validate DSL syntax without generating output."""

    try:
        flow = DotInterpreter()
        dsl_content = dsl_file.read()
        flow.parse_dsl(dsl_content)

        click.echo("✅ DSL syntax is valid!")
        click.echo(f"Found {len(flow.nodes)} nodes and {len(flow.edges)} edges")

        # Show summary
        if flow.nodes:
            click.echo("\nNodes:")
            for node_id, node in flow.nodes.items():
                click.echo(f"  - {node_id} ({node.shape.value}): {node.label}")

        if flow.edges:
            click.echo("\nEdges:")
            for edge in flow.edges:
                label_info = f" : {edge.label}" if edge.label else ""
                click.echo(f"  - {edge.from_node} -> {edge.to_node}{label_info}")

    except DotFlowError as e:
        click.echo(f"❌ DSL validation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def themes():
    """List available color themes."""
    click.echo("🎨 Available Themes:")
    click.echo("")

    for theme in Theme:
        flow = DotInterpreter(theme=theme)
        flow.start("Sample").process("Node").end("End")

        click.echo(f"  {theme.value:<12} - {_get_theme_description(theme)}")

    click.echo("")
    click.echo("Use: dotflow generate --theme THEME_NAME")


def _get_theme_description(theme: Theme) -> str:
    """Get description for a theme."""
    descriptions = {
        Theme.DEFAULT: "Clean black and white",
        Theme.DARK: "Dark mode with light text",
        Theme.COLORFUL: "Bright yellow nodes",
        Theme.BLUE: "Blue color scheme",
        Theme.GREEN: "Green color scheme",
        Theme.MONOCHROME: "Simple monochrome",
    }
    return descriptions.get(theme, "Custom theme")


@cli.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["png", "svg", "pdf", "dot"]),
    default="png",
    help="Output format",
)
@click.option(
    "--theme",
    "-t",
    type=click.Choice([t.value for t in Theme]),
    default="default",
    help="Color theme",
)
def examples(format: str, theme: str):
    """Generate example diagrams."""

    examples_dir = Path("dotflow_examples")
    examples_dir.mkdir(exist_ok=True)

    examples_data = [
        ("simple_flow", _create_simple_flow),
        ("decision_tree", _create_decision_tree),
        ("with_clusters", _create_clustered_flow),
        ("complex_workflow", _create_complex_workflow),
    ]

    for example_name, creator_func in examples_data:
        try:
            flow = DotInterpreter(example_name, Theme(theme))
            creator_func(flow)

            if format == "dot":
                output_path = examples_dir / f"{example_name}.dot"
                DotExporter().export(flow.to_dot(), str(output_path))
            else:
                output_path = examples_dir / f"{example_name}.{format}"
                ImageExporter().export(flow.to_dot(), str(output_path), format)

            click.echo(f"✓ Generated {example_name}: {output_path}")

        except Exception as e:
            click.echo(f"✗ Failed to generate {example_name}: {e}", err=True)


def _create_simple_flow(flow: DotInterpreter):
    """Create a simple linear flow."""
    (flow.start("Start").process("Step 1").process("Step 2").end("End"))


def _create_decision_tree(flow: DotInterpreter):
    """Create a decision tree flow."""
    (
        flow.start("Start")
        .process("Input Data")
        .decision("Valid?")
        .connect("Valid?", "Process Data", label="Yes")
        .connect("Valid?", "Error Handling", label="No")
        .process("Process Data")
        .decision("Success?")
        .connect("Success?", "End", label="Yes")
        .connect("Success?", "Error Handling", label="No")
        .process("Error Handling")
        .end("End")
    )


def _create_clustered_flow(flow: DotInterpreter):
    """Create a flow with clusters."""
    with flow.cluster("input", "Input Processing"):
        flow.start("Read Input").process("Validate Input")

    with flow.cluster("processing", "Data Processing"):
        flow.process("Transform").process("Analyze")

    with flow.cluster("output", "Output"):
        flow.process("Generate Report").end("Finish")

    flow.connect("Validate Input", "Transform")
    flow.connect("Transform", "Analyze")
    flow.connect("Analyze", "Generate Report")


def _create_complex_workflow(flow: DotInterpreter):
    """Create a complex workflow with multiple paths."""
    (
        flow.start("Init")
        .process("Load Config")
        .decision("Config Valid?")
        .connect("Config Valid?", "Read Data", label="Yes")
        .connect("Config Valid?", "Init", label="No")
        .process("Read Data")
        .decision("Data Available?")
        .connect("Data Available?", "Process Records", label="Yes")
        .connect("Data Available?", "End", label="No")
        .process("Process Records")
        .decision("All Processed?")
        .connect("All Processed?", "Generate Output", label="Yes")
        .connect("All Processed?", "Process Records", label="No")
        .process("Generate Output")
        .decision("Output Valid?")
        .connect("Output Valid?", "Save Results", label="Yes")
        .connect("Output Valid?", "Process Records", label="No")
        .process("Save Results")
        .end("End")
    )


@cli.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["png", "svg", "pdf", "dot"]),
    default="png",
    help="Output format",
)
def cheat_sheet(format: str):
    """Generate a DSL cheat sheet diagram."""

    flow = DotInterpreter("cheat_sheet", Theme.DEFAULT)

    dsl_examples = [
        "A -> B",
        "A -> B : Label",
        "A {decision} -> B : Yes",
        "A [shape=rect]",
        "A [shape=diamond, label='Check?']",
        "# This is a comment",
    ]

    # Create nodes for each example
    y_pos = 0
    for i, example in enumerate(dsl_examples):
        node_id = f"example_{i}"
        flow.node(node_id, example, NodeShape.RECTANGLE)
        # Simple vertical layout
        flow.set_graph_attr(f"{node_id}.pos", f"0,{y_pos}")
        y_pos -= 100

    output_path = f"dotflow_cheat_sheet.{format}"

    try:
        if format == "dot":
            DotExporter().export(flow.to_dot(), output_path)
        else:
            ImageExporter().export(flow.to_dot(), output_path, format)
    except Exception as e:
        sys.exit(f"{e}")
    click.echo(f"✓ Generated cheat sheet: {output_path}")


if __name__ == "__main__":
    cli()
