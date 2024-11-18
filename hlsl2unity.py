import re
with open('./inputHLSL/PS/Octopath_Traveler2', 'r') as file:
    content = file.read()
# print(content)
hlsl_code = content


# 示例 HLSL 代码字符串
# hlsl_code = """
# Texture2D<float4> t4 : register(t4);
# Texture2D<float4> t3 : register(t3);
# Texture2D<float4> t2 : register(t2);
# Texture2D<float4> t1 : register(t1);
# Texture2D<float4> t0 : register(t0);
# SamplerState s1_s : register(s1);
# SamplerState s0_s : register(s0); 
# cbuffer cb1 : register(b1)
# {
#   float4 cb1[8];
# }
# cbuffer cb0 : register(b0)
# {
#   float4 cb0[227];
# }
# """

# 宏定义控制是否输出结果
DEBUG_OUTPUT = True
def getHead(hlsl_code):
    # 正则表达式模式匹配 Texture2D, SamplerState, 和 cbuffer
    texture_pattern = r'Texture2D<[^>]+>\s+(\w+)\s*:\s*register\((t\d+)\);'
    sampler_pattern = r'SamplerState\s+(\w+)\s*:\s*register\((s\d+)\);'
    cbuffer_pattern = r'cbuffer\s+(\w+)\s*:\s*register\((b\d+)\)\s*\{([^}]*)\}'

    # 查找所有匹配项
    textures = re.findall(texture_pattern, hlsl_code)
    samplers = re.findall(sampler_pattern, hlsl_code)
    cbuffers = re.findall(cbuffer_pattern, hlsl_code)

    # 将匹配项存储在数组中
    texture_array = [{'name': tex[0], 'register': tex[1]} for tex in textures]
    sampler_array = [{'name': samp[0], 'register': samp[1]} for samp in samplers]
    cbuffer_array = [
        {
            'name': cbuf[0],
            'register': cbuf[1],
            'contents': [content.strip() for content in re.split(r'\s*;\s*', cbuf[2].strip()) if content.strip()]
        }
        for cbuf in cbuffers
    ]

    if DEBUG_OUTPUT==True:
        # 输出结果
        print("Textures:")
        for texture in texture_array:
            print(f"  Name: {texture['name']}, Register: {texture['register']}")

        print("\nSamplers:")
        for sampler in sampler_array:
            print(f"  Name: {sampler['name']}, Register: {sampler['register']}")

        print("\nCBuffers:")
        for cbuffer in cbuffer_array:
            print(f"  Name: {cbuffer['name']}, Register: {cbuffer['register']}")
            print("  Contents:")
            for content in cbuffer['contents']:
                print(f"    {content}")
    

    return texture_array, sampler_array, cbuffer_array
texture_array, sampler_array , cbuffer_array = getHead(hlsl_code)


