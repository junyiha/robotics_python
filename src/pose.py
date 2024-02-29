'''
    机器人姿态相关
'''

# 机械臂控制
from cob import *

Cob = Cob()

def delta_rotation(target_rot):
    '''
        使用轴角计算两个姿态的差
    '''
    rotation_vector1 = np.array(target_rot)
    rotation_vector2 = np.array([3.1400748728138406, -0.001278210673984829, -0.0015324470036047781])

    rotation1 = Rotation.from_rotvec(rotation_vector1)
    rotation2 = Rotation.from_rotvec(rotation_vector2)

    delta = rotation1.inv() * rotation2 # 左乘逆矩阵是为了将旋转转换为差值

    axis_angle_difference = delta.as_rotvec()

    logger.info(f"轴角差: {axis_angle_difference}")

    return axis_angle_difference

def min_rotation_matrix(target_rot):
    '''
    
    '''
    rotation_vector1 = np.array(target_rot)
    rotation_vector2 = np.array([3.1400748728138406, -0.001278210673984829, -0.0015324470036047781])

    initial_quaternion = Rotation.from_rotvec(rotation_vector1).as_quat()
    target_quaternion = Rotation.from_rotvec(rotation_vector2).as_quat()

    min_rotation = Rotation.from_quat(target_quaternion * initial_quaternion.conjugate()).as_rotvec()

    logger.info(f"min rotation rotvec: {round(min_rotation[0], 3), round(min_rotation[1], 3), round(min_rotation[2], 3)}")

    return min_rotation


def catch_unit_test():
    '''
        姿态差运动测试
    '''
    # 姿态
    target_rot = [0,0,0]

    # ideal
    target_pose = [0.0257481, -0.439098, 0.0479494, 0.404435, -3.10924, 0.0442371]
    target_joint = [0.317696, -0.535186, 1.3059, 0.296916, 1.55977, 1.62965]

    # non-ideal
    # target_pose = [0.0636791, -0.432493, 0.0483354, 0.664209, 3.06471, -0.0370462]
    # target_joint = [0.406095, -0.526866, 1.31554, 0.294051, 1.56157, 2.40364]

    # 使用轴角计算两个姿态的差
    # target_rot = [0.404435, -3.10924, 0.0442371]
    target_rot[0] = target_pose[3]
    target_rot[1] = target_pose[4]
    target_rot[2] = target_pose[5]
    # delta = delta_rotation(target_rot)
    delta = min_rotation_matrix(target_rot)
    logger.info(delta)
    tmp_relative = copy.deepcopy(Cob.joint_pos)
    tmp_relative["space"] = "cartBase"
    tmp_relative["speedPercent"] = 10
    tmp_relative[3] = delta[0]
    tmp_relative[4] = delta[1]
    tmp_relative[5] = delta[2]

    pose_joint = copy.deepcopy(Cob.joint_pos)
    pose_joint["target"] = target_joint
    Cob.MoveTo(pose_joint)
    # ideal_pose_cart = copy.deepcopy(Cob.cart_pos)
    # ideal_pose_cart["rotVel"] = 0.1
    # ideal_pose_cart["target"] = [
    #     0.0257481, -0.439098, 0.0479494, 0.00679038 ,-0.03900371, -2.8818453
    # ]
    # Cob.MoveTo(ideal_pose_cart)
    # logger.info(tmp_relative["target"])
    # Cob.MoveRel(tmp_relative)

    # place_pose_joint = copy.deepcopy(Cob.joint_pos)
    # place_pose_joint["target"] = [
    #     2.389926749640857, -0.12293281242558923, 1.1494258408787226, -0.3002126671997766, 1.5704741164961755, 0.8199448362750578
    # ]  
    # Cob.MoveTo(place_pose_joint)

def test_pose_transfer():
    '''
        测试姿态控制
    '''
    ideal_pose_cart = copy.deepcopy(Cob.cart_pos)
    ideal_pose_cart["target"] = [
        0.0257481, -0.439098, 0.0479494, 0.404435, -3.10924, 0.0442371
    ]
    ideal_pose_joint = copy.deepcopy(Cob.joint_pos)
    ideal_pose_joint["target"] = [
        0.317696, -0.535186, 1.3059, 0.296916, 1.55977, 1.62965
    ]  
    rot = Rotation.from_rotvec(rotvec=[ideal_pose_cart["target"][3], ideal_pose_cart["target"][4], ideal_pose_cart["target"][5]])
    euler_vec = rot.as_euler('zyx', degrees=True)
    rotation_vector = np.array([ideal_pose_cart["target"][3], ideal_pose_cart["target"][4], ideal_pose_cart["target"][5]])
    angle = np.linalg.norm(rotation_vector)
    logger.info(f"angle: {angle}, axis: {rotation_vector / angle}")
    logger.info(f"ideal pose: euler's rx: {euler_vec[0]}, euler's ry: {euler_vec[1]}, euler's rz: {euler_vec[2]}")

    tmp_axis = rotation_vector / angle
    if tmp_axis[1] > 0:
        tmp_axis[1] = tmp_axis[1] * -1

    if tmp_axis[2] < 0:
        tmp_axis[2] = tmp_axis[2] * -1
    rotation = Rotation.from_rotvec(tmp_axis * angle)
    new_axis_angle = rotation.as_rotvec()
    logger.info(f"new axis_angle: {new_axis_angle}")
    logger.info(f"origin pose: {ideal_pose_cart['target']}")
    ideal_pose_cart["target"][3] = new_axis_angle[0]
    ideal_pose_cart["target"][4] = new_axis_angle[1]
    ideal_pose_cart["target"][5] = new_axis_angle[2]
    logger.info(f"new pose: {ideal_pose_cart['target']}\n")
    

    non_ideal_pose_cart = copy.deepcopy(Cob.cart_pos)
    non_ideal_pose_cart["target"] = [
        0.0636791, -0.432493, 0.0483354, 0.664209, 3.06471, -0.0370462
    ]
    non_ideal_pose_joint = copy.deepcopy(Cob.joint_pos)
    non_ideal_pose_joint["target"] = [
        0.406095, -0.526866, 1.31554, 0.294051, 1.56157, 2.40364
    ]  
    rot = Rotation.from_rotvec(rotvec=[non_ideal_pose_cart["target"][3], non_ideal_pose_cart["target"][4], non_ideal_pose_cart["target"][5]])
    euler_vec = rot.as_euler('zyx', degrees=True)
    rotation_vector = np.array([non_ideal_pose_cart["target"][3], non_ideal_pose_cart["target"][4], non_ideal_pose_cart["target"][5]])
    angle = np.linalg.norm(rotation_vector)
    logger.info(f"angle: {angle}, axis: {rotation_vector / angle}")
    logger.info(f"non-ideal pose: euler's rx: {euler_vec[0]}, euler's ry: {euler_vec[1]}, euler's rz: {euler_vec[2]}")

    tmp_axis = rotation_vector / angle
    if tmp_axis[1] > 0:
        tmp_axis[1] = tmp_axis[1] * -1

    if tmp_axis[2] < 0:
        tmp_axis[2] = tmp_axis[2] * -1
    rotation = Rotation.from_rotvec(tmp_axis * angle)
    new_axis_angle = rotation.as_rotvec()
    logger.info(f"new axis_angle: {new_axis_angle}")
    logger.info(f"origin pose: {non_ideal_pose_cart['target']}")
    non_ideal_pose_cart["target"][3] = new_axis_angle[0]
    non_ideal_pose_cart["target"][4] = new_axis_angle[1]
    non_ideal_pose_cart["target"][5] = new_axis_angle[2]
    logger.info(f"new pose: {non_ideal_pose_cart['target']}\n")


    place_pose_cart = copy.deepcopy(Cob.cart_pos)
    place_pose_cart["target"] = [
        0.29998247172195086, 0.15902083051142829, 0.23119962718596615, 3.1400748728138406, -0.001278210673984829, -0.0015324470036047781
    ]
    place_pose_joint = copy.deepcopy(Cob.joint_pos)
    place_pose_joint["target"] = [
        2.389926749640857, -0.12293281242558923, 1.1494258408787226, -0.3002126671997766, 1.5704741164961755, 0.8199448362750578
    ]  
    rot = Rotation.from_rotvec(rotvec=[place_pose_cart["target"][3], place_pose_cart["target"][4], place_pose_cart["target"][5]])
    euler_vec = rot.as_euler('zyx', degrees=True)
    rotation_vector = np.array([place_pose_cart["target"][3], place_pose_cart["target"][4], place_pose_cart["target"][5]])
    angle = np.linalg.norm(rotation_vector)
    logger.info(f"angle: {angle}, axis: {rotation_vector / angle}")
    logger.info(f"place pose: euler's rx: {euler_vec[0]}, euler's ry: {euler_vec[1]}, euler's rz: {euler_vec[2]}")

    Cob.MoveTo(ideal_pose_joint)
    
    tmp = copy.deepcopy(ideal_pose_cart)
    tmp["target"][3] = place_pose_cart["target"][3]
    tmp["target"][4] = place_pose_cart["target"][4]
    tmp["target"][5] = place_pose_cart["target"][5]
    Cob.MoveTo(tmp)
    
    Cob.MoveTo(place_pose_cart)
    # Cob.MoveTo(place_pose_joint)

    Cob.MoveTo(non_ideal_pose_joint)
    
    tmp = copy.deepcopy(non_ideal_pose_cart)
    tmp["target"][3] = place_pose_cart["target"][3]
    tmp["target"][4] = place_pose_cart["target"][4]
    tmp["target"][5] = place_pose_cart["target"][5]
    Cob.MoveTo(tmp)

    # Cob.MoveTo(place_pose_joint)
    Cob.MoveTo(place_pose_cart)

def test_eigen(data):
    '''
        输出旋转矩阵
    '''
    pose_data = data

    rotation = Rotation.from_rotvec(np.array([pose_data[3], pose_data[4], pose_data[5]])).as_matrix()
    logger.info(f"\n{rotation}")

    return rotation

def rotation_relative(angle, current_rotation):
    '''
        对于当前姿态 绕基底坐标系的Z轴旋转指定度数
    '''
    q_cur = Rotation.from_matrix(current_rotation).as_quat()

    rotation_axis = np.array([0,0,1])
    rotation_angle = np.radians(angle)
    logger.info(rotation_angle)

    q_rotate = Rotation.from_rotvec(rotation_angle * rotation_axis).as_quat()
    
    logger.info(rotation_angle * rotation_axis)

    q_new = q_cur * q_rotate

    pose = Rotation.from_quat(q_new).as_rotvec()

    return pose

def MoveJoint(joint):
    '''
    
    '''
    data = copy.deepcopy(Cob.joint_pos)
    data["target"] = joint

    Cob.MoveTo(data)

def MoveCart(cart):
    '''
    
    '''
    data = copy.deepcopy(Cob.cart_pos)
    data["rotVel"] = 0.2
    data["target"] = cart

    Cob.MoveTo(data)


def test_move():
    '''
    
    '''
    
    data = Cob.GetCurrentStatus()
    
    cur_cart = data[1]["Info"]["control_out"]["cartesian_frame"]
    logger.info(cur_cart)
    
    # cur_cart[5] = cur_cart[5] + np.radians(10)
    # MoveCart(cur_cart)
    

if __name__ == '__main__':
    '''

    '''

    test_move()

    pose_data = [0.0257481, -0.439098, 0.0479494, 0.404435, -3.10924, 0.0442371]
    joint_data = [0.317696, -0.535186, 1.3059, 0.296916, 1.55977, 1.62965]
    # MoveJoint(joint_data)

    # 输出旋转矩阵
    # # pose_data = [0.29998247172195086, 0.15902083051142829, 0.23119962718596615, 3.1400748728138406, -0.001278210673984829, -0.0015324470036047781]
    rotation = test_eigen(pose_data)

    # 对于当前姿态 绕基底坐标系的Z轴旋转指定度数
    new_pose = rotation_relative(10, rotation)
    
    logger.info(new_pose)
    pose_data[3] = new_pose[0]
    pose_data[4] = new_pose[1]
    pose_data[5] = new_pose[2]
    logger.info(pose_data)
    # MoveCart(pose_data)


    # 测试姿态控制
    # test_pose_transfer()

    # 姿态差运动测试
    # catch_unit_test()

    logger.info("---quit---")