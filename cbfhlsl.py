import re
import os
# import cnIns 
# 示例文件路径
def getCbfhlsl():
  file_path = './inputHLSL/PS/Octopath_Traveler2'

  # 确保文件存在
  if not os.path.exists(file_path):
      print(f"File does not exist: {file_path}")
  else:
      # 读取文件内容
      with open(file_path, 'r') as file:
          hlsl_code = file.read()

  # 使用非贪婪匹配，确保只获取最小的匹配项
  pattern = r'cb[0-9]*\[[0-9]*\]'

  matches = re.findall(pattern, hlsl_code)

  strings=matches
  # 去重
  unique_strings = list(set(strings))

  # 使用字典来存储分组后的字符串
  grouped_strings = {}

  # 解析字符串并分组
  for s in unique_strings:
      # 提取`cb`后面的数字标识符
      cb_number = s.split('[')[0][2:]
      
      # 将字符串加入对应的分组
      if cb_number not in grouped_strings:
          grouped_strings[cb_number] = []
      grouped_strings[cb_number].append(s)

  # 对每个分组内的字符串进行排序
  sorted_groups = {}
  for key, group in grouped_strings.items():
      sorted_groups[key] = sorted(group)

  # 按照分组的键（即`cb`后面的数字标识符）排序后合并结果
  result = []
  for key in sorted(sorted_groups.keys(), key=lambda x: int(x)):
      result.extend(sorted_groups[key])

  # 按照分组的键（即`cb`后面的数字）排序后合并结果
  result = []
  for key in sorted(sorted_groups.keys()):
      result.extend(sorted_groups[key])

  # 输出最终结果
  # print(result)

  # for match in result:
  #     print(match)
  print(sorted_groups)
  end = []

  # 遍历字典的每一个键值对
  for key, value_list in sorted_groups.items():
      
      # print(f"Key {key}:")
      # 遍历每一个列表中的值
      for value in value_list:
          end.append(value)
          print(f"float4 {value} = ")
  print(end)
  return end
# getCbfhlsl()