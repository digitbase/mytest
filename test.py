from datetime import datetime, timedelta
from tuser import prm,prd,pres
from collections import defaultdict
from decimal import Decimal

child_space_names_array = ['管培中心', '许昌', '南阳', '平顶山', '漯河', '三门峡', '洛阳', '技培中心', '郑州', '濮阳']


subtotals_array = [
    [177.927, 0, 0, 0, 1, 0, 0, 0, 0, 5],
    [1537299100, 0, 0, 0, 0, 3, 0, 0, 0, 4],
    [1537299100, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    # Add more arrays if needed
]


accumulated_values = defaultdict(Decimal)

# 遍历 subtotals_array 并累加值
for subtotal_array in subtotals_array:
    for location, value in zip(child_space_names_array, subtotal_array):
        accumulated_values[location] += Decimal(value)

# 将字典转换为元组列表
total_usage_list = list(accumulated_values.items())

# 根据总用量排序列表
sorted_total_usage = sorted(total_usage_list, key=lambda x: x[1], reverse=True)

# 加入排名信息
ranked_total_usage = [(i+1, location, total_usage) for i, (location, total_usage) in enumerate(sorted_total_usage)]


prm(ranked_total_usage)
# 输出排序后的结果
for rank, location, total_usage in ranked_total_usage:
    print(f"排名 {rank}: {location}: {total_usage}")