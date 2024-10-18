import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.parameter import Parameter


class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.declare_parameter('text', 'Hello, ROS2!')
        self.declare_parameter('topic_name', '/spgc/receiver')
        text = self.get_parameter('text').get_parameter_value().string_value
        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        self.publisher_ = self.create_publisher(String, topic_name, 10)
        timer_period = 2.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.msg = String()
        self.msg.data = text

    def timer_callback(self):
        self.publisher_.publish(self.msg)
        self.get_logger().info(self.msg.data)


def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()