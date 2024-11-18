Shader "Unlit URP Shader"
{
Properties
{
_BaseColor("Base Color", Color) = (1,1,1,1)
_BaseMap("BaseMap", 2D) = "white" {}
}
SubShader
{
Tags { "Queue"="Geometry" "RenderType"="Opaque" "IgnoreProjector"="True" "RenderPipeline"="UniversalPipeline" }
LOD 100

Pass
{
Name "Unlit"
HLSLPROGRAM
// Required to compile gles 2.0 with standard srp library
#pragma prefer_hlslcc gles
#pragma exclude_renderers d3d11_9x
#pragma vertex vert
#pragma fragment frag
#pragma multi_compile_fog

#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/UnityInstancing.hlsl"

struct Attributes
{
float4 positionOS : POSITION;
float2 uv : TEXCOORD0;
};

struct Varyings
{
float4 positionCS : SV_POSITION;
float2 uv : TEXCOORD0;
float fogCoord : TEXCOORD1;
};

CBUFFER_START(UnityPerMaterial)
half4 _BaseColor;
float4 _BaseMap_ST;
CBUFFER_END

TEXTURE2D(_BaseMap);
SAMPLER(sampler_BaseMap);

Varyings vert(Attributes v)
{
Varyings o;
o.positionCS = TransformObjectToHClip(v.positionOS.xyz);
o.uv = TRANSFORM_TEX(v.uv, _BaseMap);
o.fogCoord = ComputeFogFactor(o.positionCS.z);
return o;
}

half4 frag(Varyings i) : SV_Target
{
half4 c;
half4 baseMap = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, i.uv);
c = baseMap * _BaseColor;
c.rgb = MixFog(c.rgb, i.fogCoord);
return c;
}
ENDHLSL
}
}
}