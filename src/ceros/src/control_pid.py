#!/usr/bin/env python

import rospy								#Importa Rospy
from std_msgs.msg import String						#Importa funciones de STRING
from geometry_msgs.msg import Twist   					#Importa lo que sern nuestros OUTPUT
from nav_msgs.msg import Odometry					#Importa ODOMETRiA IMPUTS
from ceros.msg import State						#Importa STATE de del mensaje tipo CEROS
from math import sin, cos, sqrt, pow, atan2				#Importa funciones matemticas

import time

pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=10)
pub_state = rospy.Publisher('/control/state', State, queue_size=10)
twist = Twist()
state = State()
rospy.init_node('controller', anonymous=True)


def current_milli_time():
	return round(time.time()*1000)

ant_t=0.0
err_acz=0.0
max_sat=0.4
min_sat=-0.4
goal=False
bebop2_x=0
bebop2_y=0
bebop2_z=0
bebop2_theta=0

Wx=rospy.get_param('Wx',3)	#Valor X de WAYPOINT
Wy=rospy.get_param('Wy',0)	#Valor Y de WAYPOINT
Wz=rospy.get_param('Wz',3)	#Valor Z de WAYPOINT

Kp=rospy.get_param('Kp',1)	#Ganancia proporcional
Kd=rospy.get_param('Kd',1)	#Ganancia derivativa 
Ki=rospy.get_param('Ki',1)	#Ganancia integral 	

thresh_x=rospy.get_param('~thresh_z',0.5)				#Si llega al 10% del objetivo se considera como alcanzado
thresh_y=rospy.get_param('~thresh_y',0.5)
thresh_z=rospy.get_param('~thresh_z',0.5)

rate = rospy.Rate(rospy.get_param('~hz',100))			#Frecuencia con la que publicamos

def callback(data):						#Callback para obtener la pose 
	global bebop2_x,bebop2_y,bebop2_theta, bebop2_z		
	bebop2_x = data.pose.pose.position.x			#Sacamos la posicion en X
	bebop2_y = data.pose.pose.position.y			#Sacamos la posicion en Y
	bebop2_z = data.pose.pose.position.z			#Sacamos la posicion en Z
	bebop2_theta=data.pose.pose.orientation.w		#Sacamos la orientacion en Yaw 
	#rospy.loginfo("cb:")					#Habria que descomentar todo esto?VVVVVV
	rospy.loginfo("bebop2_x:")		
	rospy.loginfo(bebop2_x)
	rospy.loginfo("bebop2_y:")		
	rospy.loginfo(bebop2_y)				#-------	
	rospy.loginfo("bebop2_z:")				#Muestra el parmetro bebop2_z		
	rospy.loginfo(bebop2_z)
	

rospy.Subscriber("/bebop/odom", Odometry, callback)		#Nos subscribimos la odometria del Dron

def listnener():
	rospy.spin()

def control():							#----Funcion de control en Z----#
	rospy.loginfo("control:")
	while not rospy.is_shutdown():
		global goal, error_z,error_x, error_y, twist, Wx, Wy,max_sat,min_sat, Wz, bebop2_x, bebop2_y, bebop2_theta, bebop2_z, ant_t,err_acz

		t=current_milli_time()
		inct=float(t-ant_t)	
		#>>goal_z=False
		#>>goal_y=False
		goal_x=False		
		rospy.loginfo("WX:")
		rospy.loginfo(Wx)
		rospy.loginfo("WY:")
		rospy.loginfo(Wy)
		rospy.loginfo("WZ:")
		rospy.loginfo(Wz)

		error_x = abs(Wx-bebop2_x)				#distancia final = sqrt( pow(Wx - bebop2_x,2) + pow(Wy - bebop2_y,2) )	
		rospy.loginfo("error_x:")		
		rospy.loginfo(error_x)
		error_y = abs(Wy-bebop2_y)					
		rospy.loginfo("error_y:")		
		rospy.loginfo(error_y)
		error_z = abs(Wz-bebop2_z)	
		rospy.loginfo("error_z:")		
		rospy.loginfo(error_z)
		
		rospy.loginfo("----------")
		

		#ESTO ES EL CONTROL EN X E Y SIN IMPLEMENTAR EL PID EN ELLOS
		if error_x < thresh_x:		#Si la distancia es menor que el umbral			
			global twist
			goal_x = True
			twist.angular.x= 0
		else :
			goal_x = False
			if Wx > bebop2_x:
				rospy.loginfo("Wx>tx")	
				twist.linear.x =Kp*error_x
			else:
				twist.linear.x = -Kp*error_x	
		if twist.linear.x > max_sat:				#He cambiado el 0.4 por una variable global llamada max_sat y min_sat
			twist.linear.x = max_sat
		if twist.linear.x < min_sat:
			twist.linear.x = min_sat	
		
		
		if error_y < thresh_y:		#Si la distancia es menor que el umbral			
			global twist
			goal_y = True
			twist.angular.y=0
		else :
			goal_y = False
			if Wy > bebop2_y:
				rospy.loginfo("Wy>ty")	
				twist.linear.y =Kp*error_y
			else:
				twist.linear.y =-Kp*error_y
		if twist.linear.y > max_sat:				#He cambiado el 0.4 por una variable global llamada max_sat y min_sat
			twist.linear.y = max_sat
		if twist.linear.y < min_sat:
			twist.linear.y = min_sat		
		
		dt=float(inct);#float(dt)=inct;
		err_acz=err_acz+error_z*dt				#Definimos el error actual.

		if error_z < thresh_z:		#Si la distancia es menor que el umbral			
			global twist
			goal_z = True 
			twist.linear.z= 0 
			twist.angular.z= 0 #<<Fragmento sin modificar, DUDA No seria velocidad lineal en vez de angular			
		else :
			goal_z = False
			if Wz > bebop2_z:
				rospy.loginfo("Wx>tx")	
				twist.linear.z =Kp*error_z
			else:
				twist.linear.z =-Kp*error_z
				#twist.linear.z = Kp*error_z+Ki*err_acz+Kd*(error_z-ant_error_z)/dt             #Esto es el control PID
				#ant_error_z=error_z								#Actualizamos Error Anterior
		if twist.linear.z > max_sat:				#He cambiado el 0.4 por una variable global llamada max_sat y min_sat
			twist.linear.z = max_sat
		if twist.linear.z < min_sat:
			twist.linear.z = min_sat	
		
		ant_t=current_milli_time()			#Tiempo anterior

#		state.error_x = error_x			#State es una estructura que contiene distancias, posiones actuales y goal
#		state.error_y = error_y		
#		state.error_z = error_z
#		state.goal=goal_z*goal_y*goal_x		#Si ha llegado o no, //deberia estar la posicion actual y la objetivo///
		
#		state.px=bebop2_x
#		state.py=bebop2_y
#		state.pz=bebop2_z
#		pub_state.publish(state)			#Publicamos
			
		pub.publish(twist)
		rospy.loginfo("Estado del control:")		#Mensaje para imprimir el estado y la velocidad que aplicamos
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
