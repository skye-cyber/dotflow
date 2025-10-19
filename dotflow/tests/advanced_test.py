from dotflow import create_flow


def create_microservices_architecture():
    # Create the main flow
    flow = create_flow("MicroserviceArchitecture", theme="blue")
    flow.direction = "TB"
    # flow.set_option("compound", True)

    # Define all nodes with specific properties
    # User-Facing Services
    api_gateway = flow.node(
        node_id="API_Gateway",
        shape="rectangle",
        style="rounded,filled",
        fillcolor="#d5f5e3",
        label="API Gateway\n(Routing/Auth)",
    )
    user_service = flow.node("User_Service", shape="component", label="User Service")
    auth_service = flow.node("Auth_Service", shape="component", label="Auth Service")

    # Core Business Services
    order_service = flow.node("Order_Service", shape="component", label="Order Service")
    payment_service = flow.node(
        "Payment_Service", shape="component", label="Payment Service"
    )
    inventory_service = flow.node(
        "Inventory_Service", shape="component", label="Inventory Service"
    )

    # Data & Support Services
    analytics_service = flow.node(
        "Analytics_Service", shape="component", label="Analytics Service"
    )
    notification_service = flow.node(
        "Notification_Service", shape="component", label="Notification Service"
    )

    # Databases
    user_db = flow.node("User_DB", shape="cylinder", label="User DB")
    order_db = flow.node("Order_DB", shape="cylinder", label="Order DB")

    # External Systems
    external_gateway = flow.node(
        "External_Payment_Gateway",
        shape="rectangle",
        style="rounded,dashed",
        label="Stripe/PayPal",
    )
    user_node = flow.node(
        "User", label="User", shape="circle", fillcolor="#aed6f1", style="filled"
    )

    # Create clusters (logical groupings)
    user_cluster = flow.cluster(
        "user_services",
        label="User-Facing Services",
        style="filled",
        color="lightgrey",
        fillcolor="#e8f4fd",
    )
    # user_cluster.add_nodes([api_gateway, user_service, auth_service])

    core_cluster = flow.cluster(
        "core_services",
        label="Core Business Services",
        style="filled",
        color="lightgrey",
        fillcolor="#fdebd0",
    )
    # core_cluster.add_nodes([order_service, payment_service, inventory_service])

    data_cluster = flow.cluster(
        "data_services",
        label="Data & Support Services",
        style="filled",
        color="lightgrey",
        fillcolor="#fadbd8",
    )
    # data_cluster.add_nodes([analytics_service, notification_service])

    # Add database sub-cluster within data cluster
    db_cluster = flow.cluster("databases", label="Databases", color="black")
    # db_cluster.add_nodes([user_db, order_db])
    # data_cluster.add_subcluster(db_cluster)

    # Add all clusters to the flow
    # flow.add_clusters([user_cluster, core_cluster, data_cluster])

    # Add external nodes
    # flow.add_nodes([external_gateway, user_node])

    # Define connections with proper labels and styles
    # Primary User Flow
    flow.connect(user_node, api_gateway, label="HTTP Request")

    # Internal Service Communications
    flow.connect(api_gateway, user_service, label="user_services")
    flow.connect(api_gateway, auth_service, style="dashed", label="JWT Validate")

    flow.connect(user_service, user_db, arrowhead="obox", label="CRUD")
    flow.connect(auth_service, user_db, arrowhead="obox", label="Auth Check")

    flow.connect(api_gateway, order_service, label="Create Order")
    flow.connect(order_service, payment_service, label="Process Payment")
    flow.connect(order_service, inventory_service, label="Check Stock")
    flow.connect(order_service, order_db, arrowhead="obox", label="Persist")

    flow.connect(payment_service, external_gateway, style="dashed", label="API Call")

    # Async Events & Notifications (dotted lines)
    flow.connect(
        order_service,
        analytics_service,
        style="dotted",
        color="blue",
        label="Order Placed (Event)",
    )
    flow.connect(
        order_service,
        notification_service,
        style="dotted",
        color="green",
        label="Send Confirmation",
    )
    flow.connect(
        payment_service,
        notification_service,
        style="dotted",
        color="green",
        label="Payment Receipt",
    )

    return flow


def main():
    # Create the architecture
    architecture = create_microservices_architecture()

    # Render to multiple formats
    architecture.render("png", "microservices_pythonic.png")
    architecture.render("svg", "microservices_pythonic.svg")
    architecture.render("pdf", "microservices_pythonic.pdf")
    architecture.render("dot", "microservices_pythonic.dot")
    print("Advanced microservices architecture generated successfully!")
    print("Files created: microservices_pythonic.png, [.svg, .pdf]")


if __name__ == "__main__":
    main()
