# umi_student_functions.py 
# In this file, we implemented the movements of the UMI RTX robotic arm  
# Babette Mooij, 10740414
# Merijn Testroote, 11173106
# Groep D
# 16-06-2017

"""
For this project we have implemented inverse kinematics in order to
let the robot arm reach the correct places. In this process
we discovered that the arm cannot reach a multitude of places on the 
chessboard in default position (0.15,-0.15, 0) such as A8. 
We have translated the board to (0.25, -0.25) in order to show a full reach,
we also rotated the board by 30 degrees to show the completeness of the 
reverse kinematica and translation functions. In the umi_simulation.py file we added a
"Play chess" button, this starts the process of playing chess through the interface we have developed last week. Note: The play chess process is AI vs AI.
During the move calculation the interace is unresponsive, we also noted that the 
game can be watched for multiple hours but at other configurations crashes after some time.
The play chess is thus a beta/fun feature.
"""

from __future__ import division, print_function
from umi_parameters import UMI_parameters
from umi_common import *
import math
import numpy as np
from visual import *
from scipy import optimize

# Specifications of UMI
UMI = UMI_parameters()

def apply_inverse_kinematics(x, y, z, gripper, board_angle, rest_state=False):
    ''' 
        Computes the angles, given some real world coordinates

        :param float x: cartesian x-coordinate
        :param float y: cartesian y-coordinate
        :param float z: cartesian z-coordinate
        :param float gripper: width of opening of the gripper
        :param float board_angle: chessboard angle
        :param boolean rest_state: states if the arm is currently doing a move

        :return: a tuple containing the position and angles of the robot-arm joints.
    '''
    # Real arm runs from of 0 to 1.082
    riser_position = y + UMI.total_arm_height 

    if rest_state == True:
        return (riser_position, 0, 0, -90, gripper)
   
    def to_solve(t):
        # Make sure the angles are in the allowed ranges
        if UMI.joint_ranges["Shoulder"][0] > degrees(t[0]) or\
           UMI.joint_ranges["Shoulder"][1] < degrees(t[0]) or\
           UMI.joint_ranges["Elbow"][0] > degrees(t[1]) or\
           UMI.joint_ranges["Elbow"][1] < degrees(t[1]):
            return [100000,100000]

        return [((UMI.upper_length * cos(t[0]) + UMI.lower_length * cos(t[0] + t[1])) - x),
                ((UMI.upper_length * sin(t[0]) + UMI.lower_length * sin(t[0] + t[1])) - z)]

    # Solve the angles using the hybr algorithm 
    theta = optimize.root(to_solve, [1,1], method='hybr')

    # The angles do not exists for all board locations
    if not theta.success:
        print("Could not find matching coords")

    theta = theta.x
    shoulder_angle = degrees(theta[0])
    elbow_angle = degrees(theta[1])

    # We want the piece to be placed down in the same angle as we picked it up
    wrist_angle = -shoulder_angle - elbow_angle + board_angle

    return (riser_position, shoulder_angle, elbow_angle, wrist_angle, gripper)



def board_position_to_cartesian(chessboard, position):
    ''' 
        Convert a position between [a1-h8] to its cartesian coordinates 
        in frameworld coordinates.

        :param obj chessboard: The instantiation of the chessboard that is used
        :param str position: A position in the range [a1-h8]

        :return: tuple Return a position in the format (x,y,z)
    '''
    # Get the local coordinates for the tiles on the board in the 0-7 range.
    (row, column) = to_coordinate(position)

    # Get information of chessboard
    chess_pos = chessboard.get_position()
    chess_angle = -chessboard.get_angle_radians()

    cos_theta = cos(chess_angle)
    sin_theta = sin(chess_angle)

    # Transformation matrix
    world_to_chess = array([
                    [cos_theta, 0,  sin_theta, chess_pos[0]],
                    [0, 1, 0, chess_pos[1]],
                    [-sin_theta, 0, cos_theta, chess_pos[2]],
                    [0, 0, 0, 1]])

    # Computes coordinates with respect to chessboard
    chess_coord = array([(7 - row) * chessboard.field_size + chessboard.field_size/2,
                         0,
                         (7 - column) * chessboard.field_size + chessboard.field_size/2,
                         1])

    # Computes coordinates with respect to world
    world_coordinate = dot(world_to_chess, chess_coord)

    return tuple(world_coordinate[:3])



def high_path(chessboard, from_pos, to_pos):
    ''' 
        Computes high path for the arm to move a piece between positions on the board.

        :param chessboard: Chessboard object
        :param from_pos: [a1-h8]
        :param to_pos: [a1-h8]
        
        :return: Returns a list of instructions for the GUI.
    '''
    sequence_list = []

    # We assume that 20 centimeter above the board is safe.
    safe_height = 0.2
    # We assume that 10 centimeter above the board is "low".
    low_height = 0.1

    # Define half_piece height of a piece on the from position.
    piece = chessboard.pieces[from_pos][1]
    half_piece_height = 0.5*chessboard.pieces_height[piece]
    
    # Define piece width to grip a piece
    piece_width = 0.7*chessboard.field_size
    board_angle = chessboard.get_angle_degrees()

    # Get the coordinates.
    (from_x, from_y, from_z) = board_position_to_cartesian(chessboard, from_pos)
    (to_x, to_y, to_z) = board_position_to_cartesian(chessboard, to_pos)
    
    add_next = lambda x, y, z, gripper, rest_state = False: \
        sequence_list.append(apply_inverse_kinematics(x, y, z, gripper, board_angle, rest_state))

    # Hover above the first field on SAFE height:
    add_next(from_x, 
             from_y + safe_height, 
             from_z, 
             chessboard.field_size) 

    # Hover above the first field on LOW height:
    add_next(from_x,
             from_y + low_height, 
             from_z, 
             chessboard.field_size)

    # Hover above the first field on half of the piece height:
    add_next(from_x,
             from_y + half_piece_height, 
             from_z, 
             chessboard.field_size)

    # Grip the piece
    add_next(from_x,
             from_y + half_piece_height,
             from_z,
             piece_width)

    # Give instruction to GUI to pickup piece
    sequence_list.append(["GUI", "TAKE", from_pos])

    # Hover above the first field on SAFE height keeping gripper closed:
    add_next(from_x,
             from_y + safe_height,
             from_z, 
             piece_width)

    # Move to new position on SAFE height keeping gripper closed:
    add_next(to_x,
             to_y + safe_height, 
             to_z,
             piece_width)

    # Hover above the new field on LOW height keeping gripper closed:
    add_next(to_x,
             to_y + low_height,
             to_z, 
             piece_width) 

    # Hover above the new field on half of the piece height keeping gripper closed:
    add_next(to_x,
             to_y + half_piece_height, 
             to_z, 
             piece_width)

    # Give instruction to GUI to drop piece
    sequence_list.append(["GUI", "DROP", to_pos])

    # Move to new position on SAFE height and open the gripper:
    add_next(to_x, 
             to_y + safe_height, 
             to_z, 
             chessboard.field_size)

    # Move to 
    add_next(0, 
             to_y + safe_height, 
             0, 
             0, 
             rest_state=True)

    return sequence_list


def move_to_garbage(chessboard, from_pos):
    '''
        Computes high path for arm to move a piece from position to the garbage.

        :param chessboard: Chessboard object
        :param from_pos: [a1-h8]

        :return: Returns a list of instructions for the GUI.
    '''
    drop_location = "j5"
    return high_path(chessboard, from_pos, drop_location)
