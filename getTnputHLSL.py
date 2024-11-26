
import re
import os

class Texture2D:
    def __init__(self, type: str, name: str, register: str):
        self.type = type
        self.name = name
        self.register = register

class SamplerState:
    def __init__(self, name: str, register: str):
        self.name = name
        self.register = register

class CBuffer:
    def __init__(self, name: str, register: str, contents: list):
        self.name = name
        self.register = register
        self.contents = contents

def parse_textures(hlsl_code: str) -> list:
    texture_pattern = r'Texture2D<([^>]+)>\s+(\w+)\s*:\s*register\((t\d+)\);'
    matches = re.findall(texture_pattern, hlsl_code)
    return [Texture2D(type=match[0], name=match[1], register=match[2]) for match in matches]

def parse_samplers(hlsl_code: str) -> list:
    sampler_pattern = r'SamplerState\s+(\w+)\s*:\s*register\((s\d+)\);'
    matches = re.findall(sampler_pattern, hlsl_code)
    return [SamplerState(name=match[0], register=match[1]) for match in matches]

def parse_cbuffers(hlsl_code: str) -> list:
    cbuffer_pattern = r'cbuffer\s+(\w+)\s*:\s*register\((b\d+)\)\s*\{([^}]*)\}'
    matches = re.findall(cbuffer_pattern, hlsl_code)
    cbuffers = []
    for match in matches:
        contents = [content.strip() for content in re.split(r'\s*;\s*', match[2].strip()) if content.strip()]
        cbuffers.append(CBuffer(name=match[0], register=match[1], contents=contents))
    return cbuffers

def parse_main_function(hlsl_code: str) -> dict:
    main_pattern = r'void\s+main\((.*?)\)\s*\{(.*?)\}'
    match = re.search(main_pattern, hlsl_code, re.DOTALL)
    
    if not match:
        print("No main function found.")
        return None
    
    parameters = match.group(1).strip()
    body_content = match.group(2).strip()
    
    input_output_split = re.split(r',\s*out\s+', parameters)
    inputs = input_output_split[0].strip().split(',')
    outputs = []
    
    if len(input_output_split) > 1:
        outputs = [f"out {param}" for param in input_output_split[1].strip().split(',')]
    
    inputs = [param.strip() for param in inputs if param.strip()]
    outputs = [param.strip() for param in outputs if param.strip()]
    
    main_input = ',\n'.join(inputs)
    main_output = ',\n'.join(outputs)
    main_content = body_content
    
    return {
        'main_input': main_input,
        'main_output': main_output,
        'main_content': main_content
    }

def read_hlsl_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            hlsl_code = file.read()
        return hlsl_code
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# 示例文件路径
file_path = './inputHLSL/PS/Octopath_Traveler2'

# 确保文件存在
if not os.path.exists(file_path):
    print(f"File does not exist: {file_path}")
else:
    # 读取文件内容
    hlsl_code = read_hlsl_file(file_path)

    if hlsl_code:
        # 解析 textures
        textures = parse_textures(hlsl_code)
        
        # 解析 samplers
        samplers = parse_samplers(hlsl_code)
        
        # 解析 cbuffers
        cbuffers = parse_cbuffers(hlsl_code)
        
        # 解析 main 函数
        parsed_main = parse_main_function(hlsl_code)

        # 输出结果
        print("Textures:")
        for texture in textures:
            print(f"  Type: {texture.type}, Name: {texture.name}, Register: {texture.register}")

        print("\nSamplers:")
        for sampler in samplers:
            print(f"  Name: {sampler.name}, Register: {sampler.register}")

        print("\nCBuffers:")
        for cbuffer in cbuffers:
            print(f"  Name: {cbuffer.name}, Register: {cbuffer.register}")
            print("  Contents:")
            for content in cbuffer.contents:
                print(f"    {content}")

        if parsed_main:
            print("\nMain Input:")
            print(parsed_main['main_input'])
            
            print("\nMain Output:")
            print(parsed_main['main_output'])
            
            print("\nMain Content:")
            # print(parsed_main['main_content'])