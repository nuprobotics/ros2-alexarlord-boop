import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class ServiceNode(Node):
    def __init__(self):
        super(ServiceNode, self).__init__('service_node')

        self.declare_parameter("service_name", "")
        self.declare_parameter("default_string", "")
        self.service_name = self.get_parameter("service_name").get_parameter_value().string_value
        self.default_string = self.get_parameter("default_string").get_parameter_value().string_value

        self.client = self.create_client(Trigger, "/spgc/trigger")
        self.string_to_store = ""
        self.service = self.create_service(Trigger, self.service_name, self.service_callback)
        if not self.client.wait_for_service(timeout_sec=1.0):
            self.string_to_store = self.default_string
        else:
            future = self.client.call_async(Trigger.Request())
            rclpy.spin_until_future_complete(self, future)
            self.string_to_store = future.result().message

    def service_callback(self, request, response):
        response.success = True
        response.message = self.string_to_store
        return response


def main():
    rclpy.init()
    node = ServiceNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
