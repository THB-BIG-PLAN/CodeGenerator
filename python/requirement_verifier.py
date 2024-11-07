# 定义操作类型常量
ACTION_ON = 1  # 表示开灯
ACTION_OFF = 0  # 表示关灯

class DeviceState:
    def __init__(self, voltage=None, current=None, temperature=None):
        # 当前状态
        self.current_state = {"voltage": voltage, "current": current, "temperature": temperature}
        # 前态状态
        self.previous_state = {"voltage": None, "current": None, "temperature": None}

    def update_state(self, voltage, current, temperature):
        """更新当前状态，并保存之前的状态为前态"""
        self.previous_state = self.current_state.copy()
        self.current_state = {"voltage": voltage, "current": current, "temperature": temperature}

    def get_current(self, param):
        """获取当前状态值"""
        return self.current_state.get(param)

    def get_previous(self, param):
        """获取前态状态值"""
        return self.previous_state.get(param)


# 定义复杂规则类
class ComplexRule:
    def __init__(self, condition, action, priority=0):
        """
        :param condition: 用于检查是否满足条件的函数
        :param action: 动作（ACTION_ON 或 ACTION_OFF）
        :param priority: 优先级，数值越小优先级越高
        """
        self.condition = condition
        self.action = action
        self.priority = priority

    def applies_to(self, device_state):
        """判断规则是否适用于当前的设备状态"""
        return self.condition(device_state)


# 冲突检测和执行函数
class ConflictDetector:
    def __init__(self, rules):
        self.rules = rules
        self.device_state = DeviceState()  # 初始化设备状态

    def detect_and_execute(self, voltage, current, temperature):
        # 更新设备状态
        self.device_state.update_state(voltage, current, temperature)

        applied_actions = self._get_applied_actions()

        if not applied_actions:
            print(f"电压 {voltage}V, 电流 {current}A, 温度 {temperature}°C 时，无规则适用")
            return False

        # 检查并处理冲突
        if self._has_conflict(applied_actions):
            print(f"冲突：电压 {voltage}V, 电流 {current}A, 温度 {temperature}°C 时，既要求开灯又要求关灯！")
            return True

        # 执行最高优先级的操作
        chosen_action = applied_actions[0][0]
        action_str = "开灯" if chosen_action == ACTION_ON else "关灯"
        print(f"电压 {voltage}V, 电流 {current}A, 温度 {temperature}°C 时，执行操作: {action_str}")
        return False

    def _get_applied_actions(self):
        """根据条件筛选适用的规则，并按优先级排序"""
        applied_actions = [
            (rule.action, rule.priority)
            for rule in self.rules
            if rule.applies_to(self.device_state)
        ]
        return sorted(applied_actions, key=lambda x: x[1])

    def _has_conflict(self, applied_actions):
        """检查是否存在开灯和关灯操作冲突"""
        actions = {action for action, _ in applied_actions}
        return ACTION_ON in actions and ACTION_OFF in actions


# 定义规则条件函数
def condition_voltage_and_current_on(device_state):
    # 检查当前状态
    current_voltage = device_state.get_current("voltage")
    current_current = device_state.get_current("current")
    previous_voltage = device_state.get_previous("voltage")
    previous_current = device_state.get_previous("current")

    # 当前电压 > 5V 且电流 > 2A，且前态不满足条件
    return (
        current_voltage > 5 and current_current > 2 and
        not (previous_voltage is not None and previous_current is not None and
             previous_voltage > 5 and previous_current > 2)
    )

def condition_voltage_and_current_off(device_state):
    # 检查当前状态
    current_voltage = device_state.get_current("voltage")
    current_current = device_state.get_current("current")
    previous_voltage = device_state.get_previous("voltage")
    previous_current = device_state.get_previous("current")

    # 当前电压 < 12V 且电流 < 3A，且前态不满足条件
    return (
        current_voltage < 12 and current_current < 3 and
        not (previous_voltage is not None and previous_current is not None and
             previous_voltage < 12 and previous_current < 3)
    )

def condition_temperature_on(device_state):
    # 检查当前温度
    current_temp = device_state.get_current("temperature")
    previous_temp = device_state.get_previous("temperature")

    # 当前温度 > 120°C 且前态不满足条件
    return (
        current_temp > 120 and
        not (previous_temp is not None and previous_temp > 120)
    )

def condition_temperature_off(device_state):
    # 检查当前温度
    current_temp = device_state.get_current("temperature")
    previous_temp = device_state.get_previous("temperature")

    # 当前温度 < 50°C 且前态不满足条件
    return (
        current_temp < 50 and
        not (previous_temp is not None and previous_temp < 50)
    )



# 定义规则列表
rules = [
    ComplexRule(condition=condition_voltage_and_current_on, action=ACTION_ON, priority=2),   # 电压>5V且电流>2A时开灯
    ComplexRule(condition=condition_voltage_and_current_off, action=ACTION_OFF, priority=3), # 电压<12V且电流<3A时关灯
    ComplexRule(condition=condition_temperature_on, action=ACTION_ON, priority=1),           # 温度>120°C时开灯
    ComplexRule(condition=condition_temperature_off, action=ACTION_OFF, priority=4)          # 温度<50°C时关灯
]

# 初始化冲突检测器并测试
detector = ConflictDetector(rules)
detector.detect_and_execute(6, 2.5, 130)  # 温度过高开灯
detector.detect_and_execute(4, 2.5, 45)   # 电压、电流和温度条件满足关灯
detector.detect_and_execute(6, 1, 125)    # 温度过高开灯
detector.detect_and_execute(13, 3, 30)    # 无规则适用
