import rclpy
from std_msgs.msg import String
from rclpy.node import Node


class Publisher(Node):
    def __init__(self):
        super(Publisher, self).__init__("publisher")
        self.declare_parameter("text", "")
        self.declare_parameter("topic_name", "")

        self.topic_name = self.get_parameter("topic_name").get_parameter_value().string_value
        self.publisher = self.create_publisher(String, self.topic_name, 10)

    def timer_callback(self):
        msg = String()
        msg.data = self.get_parameter("text").get_parameter_value().string_value
        self.publisher.publish(msg)


def main():
    rclpy.init()
    node = Publisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
