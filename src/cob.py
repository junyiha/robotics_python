'''
    机械臂测试类
'''

from network import *

class Cob:

    joint_space_speed = 30
    cart_vel = 0.2
    rot_vel  = 2

    cart_pos = {
        "space":"cartBase",
        "cartVel":cart_vel,
        "rotVel":rot_vel,
        "target":[
            0,
            0,
            0,
            0,
            0,
            0
        ]
    }
    
    joint_pos = {
        "space":"joint",
        "speedPercent":40,
        "target":[
            0,
            0,
            0,
            0,
            0,
            0
        ]  
    }

    set_tool_data = {
        "index": 1,
        "name": "tool",
        "position": [0.009114705204821452, -0.006157009004142771, 0.06917284789874306, 0.0, 0.0, 1.5707963],
        "mass": 0,
        "centerOfMass": [0, 0, 0],
        "inertia": [0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    
    delete_tool_data = {
        "index":1
    }

    set_default_data = {
        "index":1
    }

    # 通用请求
    __get_current_status = "/api/common/getCurStatus"
    __get_is_task_running = "/api/common/getIsTaskRunning"

    __get_tool = "/api/safety/getTool"
    __set_tool = "/api/safety/setTool"
    __delete_tool = "/api/safety/deleteTool"
    __set_default_tool = "/api/safety/setDefaultTool"
    
    __get_max_cart_vel = "/api/safety/getMaxCartVel"
    __get_max_joint_vel = "/api/safety/getMaxJointVel"
    __get_points = "/api/teach/getPoints"

    # 末端工具标定接口
    __add_calibrate_points = "/api/safety/tool/calibrate/addPoint"
    __get_calibrate_points = "/api/safety/tool/calibrate/getPoints"
    __clear_calibrate_points = "/api/safety/tool/calibrate/clearPoints"
    __calibrate = "/api/safety/tool/calibrate"
    __calibrate_XY_only = "/api/safety/tool/calibrateXYOnly"

    # 移动接口
    __move_to = "/api/control/moveTo"
    __move_rel = "/api/control/moveRel"


    # 内部方法
    def GetCurrentStatus(self):
        '''
            获取当前信息
        '''
        response = SendRequest(addr + self.__get_current_status)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def GetIsTaskRunning(self):
        '''
            检查机器人任务队列中是否有任务正在执行。注意，若当前队列中有任务且任务被暂停，此接口会返回True。
        '''
        response = SendRequest(addr + self.__get_is_task_running)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()
    
    def GetTool(self):
        '''
            获取末端工具
        '''
        response = SendRequest(addr + self.__get_tool)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()
    
    def SetTool(self, set_tool_data):
        '''
            设置末端工具
        '''
        response = SendRequest(addr + self.__set_tool, json.dumps(set_tool_data))
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def DeleteTool(self, delete_tool_data):
        '''
            删除末端工具
        '''
        response = SendRequest(addr + self.__delete_tool, json.dumps(delete_tool_data))
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()
    
    def SetDefaultTool(self, default_tool_data):
        '''
            设置默认工具
        '''
        response = SendRequest(addr + self.__set_default_tool, json.dumps(default_tool_data))
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def GetMaxCartVelocity(self):
        '''
            获取笛卡尔空间最大速度
        '''
        response = SendRequest(addr + self.__get_max_cart_vel)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()
    
    def GetMaxJointVelocity(self):
        '''
            获取关节空间最大速度
        '''
        response = SendRequest(addr + self.__get_max_joint_vel)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def GetPoints(self):
        '''
            获取保存的示教点
        '''
        response = SendRequest(addr + self.__get_points)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def AddCalibratePoints(self, point_array):
        '''
            设置校准点，需要将点作为参数发送给服务，每次仅设置一个，最多设置10个，超出后需要调用clear接口清空再设置
        '''
        response = SendRequest(addr + self.__add_calibrate_points, json.dumps(point_array))
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def GetCalibratePoints(self):
        '''
            获取设置的校准点，如果未设置则返回null
        '''
        response = SendRequest(addr + self.__get_calibrate_points)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def ClearCalibratePoints(self):
        '''
            清空所有已保存校准点，注：清空后无缓存，请将需要的点自行保存后再清空
        '''
        response = SendRequest(addr + self.__clear_calibrate_points)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()

    def Calibrate(self):
        '''
            根据已有校验点开始校验并获得结果，如果设置的点不足四个则失败
        '''
        response = SendRequest(addr + self.__calibrate)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()
    
    def CalibrateXYOnly(self):
        '''
            三点法工具标定
        '''
        response = SendRequest(addr + self.__calibrate_XY_only)
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()
        
    def MoveRel(self, relative_position):
        '''
            在指定空间（关节/笛卡尔基座/笛卡尔工具中心点）中做指定的相对运动。运动轨迹为对应空间中的直线
        '''
        response = SendRequest(addr + self.__move_rel, json.dumps(relative_position))
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()
    
    def MoveTo(self, position):
        '''
        
        '''
        response = SendRequest(addr + self.__move_to, json.dumps(position))
        if response.status_code != 200:
            print(f"状态码错误: {response.status_code}")
            return False
        
        return True, response.json()