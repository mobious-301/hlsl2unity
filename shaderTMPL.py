import re
import os
from cbfhlsl import *
from cbIns import *
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

class ShaderTemplate:
    shaderTMPLstr = """
Shader "MyShader/{name}"
{{
    Properties 
    {{
        {Properties}
    }}
    SubShader
    {{
        Tags
        {{
            //告诉引擎，该Shader只用于 URP 渲染管线
            "RenderPipeline"="UniversalPipeline"
            //渲染类型
            "RenderType"="Opaque"
            //渲染队列
            "Queue"="Geometry"
        }}
        Pass
        {{
            Name "Universal Forward"
            Tags
            {{
                // LightMode: <None>
            }}

            Cull Back
            Blend One Zero
            ZTest LEqual
            ZWrite On
          
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // Pragmas
            #pragma target 2.0
            
            // Includes
            #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Input.hlsl"

            CBUFFER_START(UnityPerMaterial)
            half4 _Color;
            CBUFFER_END

            
            //纹理的定义，如果是编译到GLES2.0平台，则相当于sample2D _MainTex;否则相当于 Texture2D _MainTex;
            TEXTURE2D(_MainTex);
            float4 _MainTex_ST;

            {TEXTURE2D}
            //采样器的定义，如果是编译到GLES2.0平台，就相当于空;否则相当于 SamplerState sampler_MainTex;
            //SAMPLER(sampler_MainTex);
            //修改纹理采样格式
            #define smp SamplerState_linear_mirrorU_ClampV
            SAMPLER(smp);
            {SAMPLER}
            
            //struct appdata
            //顶点着色器的输入
            struct Attributes
            {{
                float3 positionOS : POSITION;
                float2 uv : TEXCOORD0;
                
            }};
            //struct v2f
            //片元着色器的输入
            struct Varyings
            {{
                float4 positionCS : SV_POSITION;
                float2 uv : TEXCOORD0;
                
            }};
            //v2f vert(Attributes v)
            //顶点着色器
            Varyings vert(Attributes v)
            {{
                Varyings o = (Varyings)0;
                float3 positionWS = TransformObjectToWorld(v.positionOS);
                o.positionCS = TransformWorldToHClip(positionWS);
                o.uv = TRANSFORM_TEX(v.uv,_MainTex);
                return o;
            }}
            //fixed4 frag(v2f i) : SV_TARGET
            //片元着色器
            half4 frag(float4 v0 : TEXCOORD0,
                       float3 v1 : TEXCOORD1, out float4 o0 : SV_POSITION) : SV_TARGET
            {{
                half4 c;
                float4 mainTex = SAMPLE_TEXTURE2D(_MainTex,smp,v0.xy);
                c = _Color *  mainTex;
                return c;
                {frag}
            }}
            ENDHLSL
        }}
    }}

    FallBack "Hidden/Shader Graph/FallbackError"
}}
"""

    def __init__(self, name: str):
        self.name = name
        self.properties = []
        self.textures = []
        self.samplers = []
        self.cbuffers = []

        self.psCb = []

        # psCb,psCb1,psCbCon,psCbname = getcbIns()
        self.main_input = ""
        self.main_output = ""
        self.main_content = ""
    def add_psCb(self, texture):
        self.psCb.append(texture)

    def add_texture(self, texture: Texture2D):
        self.textures.append(texture)

    def add_sampler(self, sampler: SamplerState):
        self.samplers.append(sampler)

    def add_cbuffer(self, cbuffer: CBuffer):
        self.cbuffers.append(cbuffer)

    def set_main_function(self, main_input: str, main_output: str, main_content: str):
        self.main_input = main_input
        self.main_output = main_output
        self.main_content = main_content

    def generate_shader(self) -> str:
        properties_str = "\n".join([f"{tex.name} (\"{tex.name}\", 2D) = \"white\" {{}}" for tex in self.textures])

        properties_str+="\n"
        properties_str+="\n".join(shader_template.psCb[0])
        textures_str = "\n".join([f"TEXTURE2D({tex.name});" for tex in self.textures])
        samplers_str = "\n".join([f"SAMPLER({sampler.name});" for sampler in self.samplers])
        samplers_str+="\n"
        samplers_str+= "\n".join(shader_template.psCb[1])

        frag_str="\n".join(self.psCb[2])+"\n"

        frag_str += self.main_content

        shader_str = self.shaderTMPLstr.format(
            name=self.name,
            Properties=properties_str,
            TEXTURE2D=textures_str,
            SAMPLER=samplers_str,
            frag=frag_str
        )
        return shader_str

def parse_textures(hlsl_code: str) -> list:
    texture_pattern = r'Texture2D<([^>]+)>\s+(\w+)\s*:\s*register\((t\d+)\);'
    matches = re.findall(texture_pattern, hlsl_code)
    return [Texture2D(type=match[0], name=f"_t{i}", register=match[2]) for i, match in enumerate(matches)]

def parse_samplers(hlsl_code: str) -> list:
    sampler_pattern = r'SamplerState\s+(\w+)\s*:\s*register\((s\d+)\);'
    matches = re.findall(sampler_pattern, hlsl_code)
    return [SamplerState(name=f"s{i}", register=match[1]) for i, match in enumerate(matches)]

def parse_cbuffers(hlsl_code: str) -> list:
    cbuffer_pattern = r'cbuffer\s+(\w+)\s*:\s*register\((b\d+)\)\s*\{([^}]*)\}'
    matches = re.findall(cbuffer_pattern, hlsl_code)
    cbuffers = []
    for match in matches:
        contents = [content.strip() for content in re.split(r'\s*;\s*', match[2].strip()) if content.strip()]
        cbuffers.append(CBuffer(name=match[0], register=match[1], contents=contents))
    return cbuffers

def parse_main_function(hlsl_code: str) -> dict:
    main_pattern = r'void\s+main\((.*?)\)\s*\{(.*)?'
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

def replace_sample_level(main_content: str, textures: list) -> str:
    sample_level_pattern = r'(r\s+\S+)= (\s+\S+).SampleLevel\(\s+\S+s, (\s+\S+), [\s\S]\)' #性能问题
    step_cmp_greater_equal_pattern = r'(r[\s\S]*?)= cmp\(([\s\S]*?) [=]*>[=]* ([\s\S]*?)\);'
    step_cmp_less_equal_pattern = r'(r[\s\S]*?)= cmp\(([\s\S]*?) [=]*<[=]* ([\s\S]*?)\);'


    sample_level_pattern = r'= (.*).SampleLevel\(.*?_s,(.*)?,.*?\)'
    sampleload = r'= (.*)\.Load'

    # =.*\.load

    main_content = re.sub(sample_level_pattern, rf'= SAMPLE_TEXTURE2D(_\1, smp, \2)', main_content)

    # Replace cmp(x >= y) with step(y, x) - 1
    main_content = re.sub(step_cmp_greater_equal_pattern, rf'\1 = step(\3 , \2)-1;', main_content)
    # Replace cmp(x <= y) with step(x, y) - 1
    main_content = re.sub(step_cmp_less_equal_pattern, rf'\1 = step(\2 , \3)-1;', main_content)
    main_content =  re.sub(sampleload, rf'= _\1.Load', main_content)

    return main_content

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

        # 创建 ShaderTemplate 实例
        shader_template = ShaderTemplate(name="Octopath_Traveler2")

        # 添加 textures
        for texture in textures:
            shader_template.add_texture(texture)

        # 添加 samplers
        for sampler in samplers:
            shader_template.add_sampler(sampler)

        # 添加 cbuffers
        for cbuffer in cbuffers:
            shader_template.add_cbuffer(cbuffer)

            
        psCb,psCb1,psCbCon,psCbname = getcbIns()
        shader_template.add_psCb(psCb)
        shader_template.add_psCb(psCb1)
        shader_template.add_psCb(psCbCon)
        shader_template.add_psCb(psCbname)
        print("sva")
        print(shader_template.psCb[0])

        # 设置 main 函数
        if parsed_main:
            main_content = replace_sample_level(parsed_main['main_content'], textures)
            shader_template.set_main_function(
                main_input=parsed_main['main_input'],
                main_output=parsed_main['main_output'],
                main_content=main_content
            )

        # 生成 Shader 字符串
        generated_shader = shader_template.generate_shader()

        # 输出生成的 Shader 字符串
        # print(generated_shader)



        # file_path='./outputShaders/Octopath_Traveler2_Shader.shader'
        file_path='./a-2 case1'


                # 获取目录名
        directory = os.path.dirname(file_path)

        # 如果目录不存在，则创建
        if not os.path.exists(directory):
            os.makedirs(directory)


        # 可选：将生成的 Shader 写入文件
        with open(file_path, 'w') as shader_file:
            shader_file.write(generated_shader)






