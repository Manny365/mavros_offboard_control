#!/usr/bin/env python

import rospy
import mavros
import sensor_msgs
import yaml
#from mavros.msg import *
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix

#global variables
latitude = 0.0
longitude = 0.0
altitude = 0.0
last_waypoint = False

def waypoint_callback(data):
	global last_waypoint
	#print("\n----------\nwaypoint_callback")
	rospy.loginfo("Got waypoint: %s", data)
	if len(data.waypoints) != 0:							#if waypoint list is not empty
		rospy.loginfo("is_current: %s", data.waypoints[len(data.waypoints)-1].is_current)
		last_waypoint = data.waypoints[len(data.waypoints)-1].is_current	#checks status of "is_current" for last waypoint

def globalPosition_callback(data):
	#print("\n----------\nglobalPosition_callback")
	global latitude
	global longitude
	global altitude
	latitude = data.latitude
	longitude = data.longitude
	altitude = data.altitude

def main():
	rospy.init_node('wayPoint')
	rospy.Subscriber("/mavros/mission/waypoints", WaypointList, waypoint_callback)
	rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPosition_callback)

	#Clearing waypoints
	print("\n----------CLEARING----------")
	rospy.wait_for_service("/mavros/mission/clear")
	print("Clearing Waypoints!!!")
	waypoint_clear = rospy.ServiceProxy("/mavros/mission/clear", WaypointClear)
	resp = waypoint_clear()
	print(resp)
	rospy.sleep(5)
	#Call waypoints_pull
	print("\n----------PULLING----------")
	rospy.wait_for_service("/mavros/mission/pull")
	print("Calling Waypoint_pull Service")
	waypoint_pull = rospy.ServiceProxy("/mavros/mission/pull", WaypointPull)
	resp = waypoint_pull()
	print(resp)
	rospy.sleep(5)
#	#Arming
#	print("\n----------ARMING----------")
#	rospy.wait_for_service("/mavros/cmd/arming")
#	print("Arming UAV!!!")
#	uav_arm = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
#	resp = uav_arm(1)
#	print(resp)
#	rospy.sleep(5)

	#Sending waypoints_push
	print("\n----------PUSHING----------")
	print("Waiting for MAVROS service...")
	rospy.wait_for_service("/mavros/mission/push")
	waypoints = [
		Waypoint(frame = 3, command = 22, is_current = True, autocontinue = True, param1 = 5, x_lat = 37.198464, y_long = -80.578876, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198344, y_long = -80.579098, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198076, y_long = -80.579170, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198103, y_long = -80.579434, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197911, y_long = -80.579580, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197722, y_long = -80.579639, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197730, y_long = -80.579824, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197622, y_long = -80.579783, z_alt = 10),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197538, y_long = -80.579725, z_alt = 5)
	]
	waypoint_push = rospy.ServiceProxy("/mavros/mission/push", WaypointPush)
	resp = waypoint_push(waypoints)
	print(resp)
	rospy.sleep(5)
	
	while True:						#waits for last_waypoint in previous WaypointList to be visited
		rospy.sleep(2)
		print("WAITING for last_waypoint == True")
		if last_waypoint == True:			#if last_waypoint is in the process of being visited
			while True:
				rospy.sleep(2)
				print("WAITING for last_waypoint == False")
				if last_waypoint == False:	#if last_waypoint has been visited (due to previous constraint)
					break
			break
	
	#Clearing waypoints
	print("\n----------CLEARING----------")
	rospy.wait_for_service("/mavros/mission/clear")
	print("Clearing Waypoints!!!")
	waypoint_clear = rospy.ServiceProxy("/mavros/mission/clear", WaypointClear)
	resp = waypoint_clear()
	print(resp)
	rospy.sleep(5)
	#Call waypoints_pull
	print("\n----------PULLING----------")
	rospy.wait_for_service("/mavros/mission/pull")
	print("Calling Waypoint_pull Service")
	waypoint_pull = rospy.ServiceProxy("/mavros/mission/pull", WaypointPull)
	resp = waypoint_pull()
	print(resp)
	rospy.sleep(5)

	while True:
		rospy.sleep(2)
		print("WAITING for us to be within 1 meter of the next takeoff point")
		#print(" lat " + repr(latitude) + " long " + repr(longitude) + " alt " + repr(altitude))
		#latlongalt = (latitude-37.1973420)+(longitude-(-80.5798929))+(altitude-529)		#checks for total difference is less than 0.0001
		if (latitude-37.197283)<0.0001 and (longitude-(-80.579970))<0.0001:
			rospy.wait_for_service("/mavros/mission/push")
			resp = waypoint_push(waypoints)
			waypoints = [
				Waypoint(frame = 3, command = 22, is_current = True, autocontinue = True, param1 = 5, x_lat = 37.197283, y_long = -80.579970, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197449, y_long = -80.580025, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197571, y_long = -80.580121, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197647, y_long = -80.579940, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197733, y_long = -80.579960, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197842, y_long = -80.580088, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197736, y_long = -80.580354, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197850, y_long = -80.580339, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197927, y_long = -80.580406, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198000, y_long = -80.580357, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198050, y_long = -80.580464, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198150, y_long = -80.580334, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198160, y_long = -80.580287, z_alt = 5)
							]
			resp = waypoint_push(waypoints)
			print(resp)
			rospy.sleep(5)
			break

	while True:						#waits for last_waypoint in previous WaypointList to be visited
		rospy.sleep(2)
		print("WAITING for last_waypoint == True")
		if last_waypoint == True:			#if last_waypoint is in the process of being visited
			while True:
				rospy.sleep(2)
				print("WAITING for last_waypoint == False")
				if last_waypoint == False:	#if last_waypoint has been visited (due to previous constraint)
					break
			break
	
	#Clearing waypoints
	print("\n----------CLEARING----------")
	rospy.wait_for_service("/mavros/mission/clear")
	print("Clearing Waypoints!!!")
	waypoint_clear = rospy.ServiceProxy("/mavros/mission/clear", WaypointClear)
	resp = waypoint_clear()
	print(resp)
	rospy.sleep(5)
	#Call waypoints_pull
	print("\n----------PULLING----------")
	rospy.wait_for_service("/mavros/mission/pull")
	print("Calling Waypoint_pull Service")
	waypoint_pull = rospy.ServiceProxy("/mavros/mission/pull", WaypointPull)
	resp = waypoint_pull()
	print(resp)
	rospy.sleep(5)

	while True:
		rospy.sleep(2)
		print("WAITING for us to be within 1 meter of the next takeoff point")
		#print(" lat " + repr(latitude) + " long " + repr(longitude) + " alt " + repr(altitude))
		if (latitude-37.198015)<0.0001 and (longitude-(-80.580266))<0.0001:
			rospy.wait_for_service("/mavros/mission/push")
			resp = waypoint_push(waypoints)
			waypoints = [
				Waypoint(frame = 3, command = 22, is_current = True, autocontinue = True, param1 = 5, x_lat = 37.198015, y_long = -80.580266, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197984, y_long = -80.580232, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197992, y_long = -80.580106, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.197994, y_long = -80.579917, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198066, y_long = -80.579928, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198109, y_long = -80.579809, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198136, y_long = -80.579748, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198264, y_long = -80.579771, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198245, y_long = -80.580000, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198277, y_long = -80.580090, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198346, y_long = -80.580144, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198403, y_long = -80.580118, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198465, y_long = -80.580150, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198608, y_long = -80.580019, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198674, y_long = -80.579916, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198440, y_long = -80.579790, z_alt = 5)
			]
			resp = waypoint_push(waypoints)
			print(resp)
			rospy.sleep(5)
			break

	while True:						#waits for last_waypoint in previous WaypointList to be visited
		rospy.sleep(2)
		print("WAITING for last_waypoint == True")
		if last_waypoint == True:			#if last_waypoint is in the process of being visited
			while True:
				rospy.sleep(2)
				print("WAITING for last_waypoint == False")
				if last_waypoint == False:	#if last_waypoint has been visited (due to previous constraint)
					break
			break
	
	#Clearing waypoints
	print("\n----------CLEARING----------")
	rospy.wait_for_service("/mavros/mission/clear")
	print("Clearing Waypoints!!!")
	waypoint_clear = rospy.ServiceProxy("/mavros/mission/clear", WaypointClear)
	resp = waypoint_clear()
	print(resp)
	rospy.sleep(5)
	#Call waypoints_pull
	print("\n----------PULLING----------")
	rospy.wait_for_service("/mavros/mission/pull")
	print("Calling Waypoint_pull Service")
	waypoint_pull = rospy.ServiceProxy("/mavros/mission/pull", WaypointPull)
	resp = waypoint_pull()
	print(resp)
	rospy.sleep(5)

	while True:
		rospy.sleep(2)
		print("WAITING for us to be within 1 meter of the next takeoff point")
		#print(" lat " + repr(latitude) + " long " + repr(longitude) + " alt " + repr(altitude))
		if (latitude-37.198354)<0.0001 and (longitude-(-80.579569))<0.0001:
			rospy.wait_for_service("/mavros/mission/push")
			resp = waypoint_push(waypoints)
			waypoints = [
				Waypoint(frame = 3, command = 22, is_current = True, autocontinue = True, param1 = 5, x_lat = 37.198354, y_long = -80.579569, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198221, y_long = -80.579553, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198306, y_long = -80.579426, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198494, y_long = -80.579398, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198658, y_long = -80.579292, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198805, y_long = -80.579098, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198895, y_long = -80.579202, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198890, y_long = -80.579250, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198899, y_long = -80.579330, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198838, y_long = -80.579339, z_alt = 10),
				Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.198850, y_long = -80.579627, z_alt = 10),
				Waypoint(frame = 3, command = 21, is_current = False, autocontinue = True, param1 = 5, x_lat = 37.199110, y_long = -80.579389, z_alt = 0)

			]
			resp = waypoint_push(waypoints)
			print(resp)
			rospy.sleep(5)
			break

	while True:						#waits for last_waypoint in previous WaypointList to be visited
		rospy.sleep(2)
		print("WAITING for last_waypoint == True")
		if last_waypoint == True:			#if last_waypoint is in the process of being visited
			while True:
				rospy.sleep(2)
				print("WAITING for last_waypoint == False")
				if last_waypoint == False:	#if last_waypoint has been visited (due to previous constraint)
					break
			break

	print("EVERYTHING WORKED AS PLANNED!!!")
	rospy.spin()

	


if __name__ == '__main__':
	main()

