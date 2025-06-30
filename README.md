# DOCS2025
DOCS2025第一届“辽河杯”数据驱动的复杂系统优化算法竞赛：柔性流水车间动态调度问题

更新记录：

6.25   新增数字签名

6.26   更新competitionPlatform，修改 run_simulation函数，仅在 isTimeout==True 时，输出数字签名

6.26   更新competitionPlatform，修复“最后一个订单到达时，无法动态调度”的问题。

6.27   更新competitionPlatform，修复Linux平台读取包错误的问题。

6.30   更新competitionPlatform，修复“getOrders函数在设置了only_unfinished=False时报错”的问题。  
       当only_unfinished=False时，已完成订单的start_time和end_time,即为订单的第一阶段的开始生产时间和最后阶段的结束时间。
