from enum import Enum


# 定义行为枚举
class Action(Enum):
    TURN_ON = "开灯"
    TURN_OFF = "关灯"


# 定义复杂规则类
class ComplexRule:
    def __init__(self, condition, action, priority=0):
        self.condition = condition  # 规则触发的多信号条件函数
        self.action = action  # 规则的行为
        self.priority = priority  # 优先级

    def applies_to(self, voltage, current):
        """判断规则是否适用于给定电压和电流"""
        return self.condition(voltage, current)


# 冲突检测函数
def detect_complex_conflicts(voltage, current, ruleArray):
    applied_actions = []  # 适用的操作列表
    conflict_detected = False

    for rule in ruleArray:
        if rule.applies_to(voltage, current):
            applied_actions.append((rule.action, rule.priority))

    # 按优先级排序
    applied_actions = sorted(applied_actions, key=lambda x: x[1], reverse=True)

    # 检查是否有相互矛盾的操作
    actions = [action for action, _ in applied_actions]
    if Action.TURN_ON in actions and Action.TURN_OFF in actions:
        conflict_detected = True
        print(f"冲突：电压 {voltage}V 和 电流 {current}A 时，既要求开灯又要求关灯！")
    else:
        if not applied_actions:
            print(f"电压 {voltage}V 和 电流 {current}A 时，无规则适用")
        else:
            # 执行优先级最高的操作
            chosen_action = applied_actions[0][0]
            print(f"电压 {voltage}V 和 电流 {current}A 时，执行操作: {chosen_action.value}")

    return conflict_detected


# 定义多信号条件函数
def voltage_and_current_condition_1(voltage, current):
    return voltage > 5 and current > 2


def voltage_and_current_condition_2(voltage, current):
    return voltage < 12 and current < 3


# 定义规则
rules = [
    ComplexRule(condition=voltage_and_current_condition_1, action=Action.TURN_ON, priority=1),  # 电压>5V且电流>2A时开灯
    ComplexRule(condition=voltage_and_current_condition_2, action=Action.TURN_OFF, priority=2)  # 电压<12V且电流<3A时关灯
]

# 测试不同的电压和电流组合
detect_complex_conflicts(6, 2.5, rules)  # 检测到冲突
detect_complex_conflicts(4, 2.5, rules)  # 关灯
detect_complex_conflicts(6, 1, rules)  # 关灯
detect_complex_conflicts(13, 3, rules)  # 开灯
