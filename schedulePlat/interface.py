import dfjsp
import pandas as pd


class Interface:
    def __init__(self, algorithm_type="random"):
        self.debug = False
        self.cpp_platform = dfjsp.Platform()
        self.scheduler = dfjsp.Scheduler()
        self.scheduler.setPlatform(self.cpp_platform)
        self.algorithm_type = algorithm_type

    def _convert_and_set_data(self, platform):
        """转换并设置数据到C++ Platform"""
        # 获取数据
        orders = platform.getOrders()
        machines_status = platform.getCurrentMachineStatus()
        MBOM = platform.getMBOM()
        current_time = platform.getSimulationTime()

        # 转换订单数据
        cpp_orders = []
        for _, row in orders.iterrows():
            order = dfjsp.OrderInfo()
            order.order_id = str(row.get('order_id', ''))
            order.product_type = str(row.get('product_type', ''))
            order.arrival_time = float(row.get('arrival_time', 0))
            order.due_date = float(row.get('due_date', 0))
            order.current_stage = str(row.get('current_stage', '')) if pd.notna(row.get('current_stage')) else ""
            order.assigned_machine = str(row.get('assigned_machine', '')) if pd.notna(
                row.get('assigned_machine')) else ""
            order.start_time = float(row.get('start_time', 0)) if pd.notna(row.get('start_time')) else 0
            order.end_time = float(row.get('end_time', 0)) if pd.notna(row.get('end_time')) else 0
            order.fulfillment_rate = float(row.get('fulfillment_rate', 0))
            cpp_orders.append(order)

        # 转换机器状态数据
        cpp_machines = []
        for machine_id, row in machines_status.iterrows():
            machine = dfjsp.MachineStatus()
            machine.machine_id = str(machine_id)
            machine.task_id = str(row.get('task_id', '')) if pd.notna(row.get('task_id')) else ""
            machine.start_time = float(row.get('start_time', 0)) if pd.notna(row.get('start_time')) else 0
            machine.end_time = float(row.get('end_time', 0)) if pd.notna(row.get('end_time')) else 0
            cpp_machines.append(machine)

        # 转换MBOM数据
        cpp_mbom = []
        for _, row in MBOM.iterrows():
            mbom = dfjsp.MBOMInfo()
            mbom.product_type = str(row.get('product_type', ''))
            mbom.stage = str(row.get('stage', ''))
            mbom.machine_id = str(row.get('machine_id', ''))
            mbom.process_time = float(row.get('process_time(s)', 0))
            cpp_mbom.append(mbom)

        # 设置数据到C++ Platform
        self.cpp_platform.setOrders(cpp_orders)
        self.cpp_platform.setMachineStatus(cpp_machines)
        self.cpp_platform.setMBOM(cpp_mbom)
        self.cpp_platform.setCurrentTime(current_time)

    def _convert_results_to_dataframe(self, cpp_results):
        """将C++结果转换为pandas DataFrame"""
        schedule_data = []
        for result in cpp_results:
            schedule_data.append({
                'task_id': result.task_id,
                'machine_id': result.machine_id,
                'start_time': result.start_time
            })
        return pd.DataFrame(schedule_data)

    def generate_schedule(self, platform) -> pd.DataFrame:
        """
        动态生成调度计划
        :param platform: 仿真测试平台
        :return: 调度计划DataFrame
        """
        # 转换并设置数据
        self._convert_and_set_data(platform)

        # 调试信息
        if hasattr(self, 'debug') and self.debug:
            print("=== C++ Platform Status ===")
            print(self.cpp_platform.getStatusSummary())
            self.cpp_platform.printOrders()
            self.cpp_platform.printMachineStatus()

        # 根据算法类型调用不同的调度方法
        if self.algorithm_type == "fifo":
            cpp_results = self.scheduler.generateScheduleFIFO()
        elif self.algorithm_type == "edd":
            cpp_results = self.scheduler.generateScheduleEDD()
        elif self.algorithm_type == "spt":
            cpp_results = self.scheduler.generateScheduleSPT()
        else:  # default: random
            cpp_results = self.scheduler.generateScheduleRandom()

        # 调试信息
        if hasattr(self, 'debug') and self.debug:
            print("=== Schedule Results ===")
            print(self.scheduler.getScheduleInfo(cpp_results))

        # 转换结果回pandas DataFrame
        return self._convert_results_to_dataframe(cpp_results)

    def enable_debug(self, debug=True):
        """启用调试模式"""
        self.debug = debug

    def set_algorithm(self, algorithm_type):
        """设置调度算法类型"""
        self.algorithm_type = algorithm_type

    def get_platform_info(self):
        """获取平台信息用于调试"""
        return self.cpp_platform.getStatusSummary()
