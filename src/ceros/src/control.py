#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from turtlesim.msg import Pose
from ceros.msg import State
from math import sin, cos, sqrt, pow, atan2

pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=10)
pub_state = rospy.Publisher('/control/state', State, queue_size=10)
twist = Twist()
state = State()
rospy.init_node('controller', anonymous=True)

goal=False
turtle_x=0
turtle_y=0
turtle_theta=0

Wx=rospy.get_param('Wx',0)	#Parametros privados
Wy=rospy.get_param('Wy',0)
Wz=rospy.get_param('Wz',1)
Pv=rospy.get_param('Pv',1)
Po=rospy.get_param('Po',2)
thresh=rospy.get_param('~thresh',0.25)
rate = rospy.Rate(rospy.get_param('~hz',10))

def callback(data):
	global turtle_x,turtle_y,turtle_theta
	turtle_x = data.pose.pose.position.x
	turtle_y = data.pose.pose.position.y
	turtle_Z = data.pose.pose.position.z
	turtle_theta=data.pose.pose.orientation.w
	rospy.loginfo("cb:")	
	rospy.loginfo("turtle_x:")		
	rospy.loginfo(turtle_x)
	rospy.loginfo("turtle_y:")		
	rospy.loginfo(turtle_y)
	

rospy.Subscriber("/bebop/odom", Odometry, callback)

def listnener():
	rospy.spin()

def control():
	rospy.loginfo("control:")
	while not rospy.is_shutdown():
		global goal, dist, ori, twist, Wx, Wy, turtle_x, turtle_y, turtle_theta
		rospy.loginfo("WX:")
		rospy.loginfo(Wx)
		dist = sqrt( pow(Wx - turtle_x,2) + pow(Wy - turtle_y,2) )
		rospy.loginfo("dist:")		
		rospy.loginfo(dist)
		rospy.loginfo("----------")
		ori = turtle_theta#ori = atan2( (Wy-turtle_y),(Wx-turtle_x) ) - turtle_theta
		if dist < thresh:
			global twist
			goal = True
			twist.linear.x = 0
			twist.angular.z= 0
		else :
			goal = False
			if Wx > turtle_x:
				rospy.loginfo("Wx>tx")	
				twist.linear.y = Pv*dist
			else:
				twist.linear.y = -Pv*dist
			twist.angular.z=0#twist.angular.z= Po*ori
		if twist.linear.y > 1:
			twist.linear.y = 1
		if twist.linear.y < -1:
			twist.linear.y = -1		
		state.dist = dist
		state.ori = ori
		state.goal=goal
		pub_state.publish(state)			
		pub.publish(twist)
		rospy.loginfo("Estado del control:")
		rospy.loginfo(state)
		print("")
		rospy.loginfo("Velocidad aplicada:")
		rospy.loginfo(twist)
		print("")
		rate.sleep()

if __name__=='__main__':
	try:
		control()
	except rospy.ROSInterruptException:
		pass
