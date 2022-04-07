#!/usr/bin/env python2
import rospy
from geometry_msgs.msg import TwistStamped, Twist
from std_msgs.msg import Empty

class InsulatorFocus:
    def __init__(self):
        self.sub_nw_output = rospy.Subscriber("/network_output", TwistStamped, self.cb_nw_output) 
        self.sub_start = rospy.Subscriber("start", Empty, self.cb_start)

        self.pub_body_vel = rospy.Publisher("/tello/cmd_vel", Twist, queue_size=10)
        self.pub_take_off = rospy.Publisher("/tello/takeoff", Empty , queue_size=1)
        
        self.rate = rospy.Rate(20)
        self.body_vel = Twist()
        self.start = False

    def cb_start(self, msg):
        self.start = True

    def cb_nw_output(self, msg):   
        self.body_vel = msg.twist

    def run(self):
        take_off_msg = Empty()
        for i in range(5):
            self.pub_take_off.publish(take_off_msg)
            rospy.loginfo("execute %d cmd", i)
            self.rate.sleep()
        rospy.sleep(5.0)
        rospy.loginfo("The tello has taken off")
        while not rospy.is_shutdown():
            t_c = rospy.get_time()
            if self.start:
                if(t_c - t_s < 5.0):
                    self.pub_body_vel.publish(self.body_vel)
                    rospy.loginfo("%f", self.body_vel.linear.x)
                else:
                    rospy.loginfo("stop the vel cmd")
                self.rate.sleep()
            else:
                t_s = t_c
                rospy.loginfo_once("wait for start command")

def main():
    rospy.init_node("insulator_foucs_tello")

    insulator_focus = InsulatorFocus()
    insulator_focus.run()

    

if __name__ == '__main__':
    main()