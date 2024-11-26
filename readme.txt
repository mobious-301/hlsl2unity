linux shell:
dot -Tpdf D:\MLearning\tree.dot -o D:\MLearning\tree.pdf 

dot -Tpdf .\hlsl.txt -o .\tree.pdf 
dot -Tpdf .\hlsl.txt -o .\tree1.pdf 


r6.xyzw = t1.SampleBias(s1_s, v3.xy, cb0[133].x).xyzw;
(r[\s\S]*)= ([\s\S]*).SampleBias\([\s\S]*s, ([\s\S]*), [\s\S]*\).([\s\S]*);
$1 = tex2D($2,$3).$4;


Octopath_Traveler2


r6.xyzw = t1.SampleLevel(s1_s, v3.xy, cb0[133].x).xyzw;
(r[\s\S]*)= ([\s\S]*).SampleLevel\([\s\S]*s, ([\s\S]*), [\s\S]*\).([\s\S]*);
$1 = SAMPLE_TEXTURE2D(_$2,$2,$3).$4;

(r[\s\S]*)= ([\s\S]*).SampleLevel\([\s\S]*s, ([\s\S]*), [\s\S]*\).([\s\S]*);
$1 $2 $3 $4 $5 $6

$1 = SAMPLE_TEXTURE2D(_$2,smp,$3).$4;
r7.xyzw = t8.SampleLevel(s2_s, v0.xy, 0).xyzw;
r7.xyzw = tSAMPLE_TEXTURE2D(t8, smp, s2_s).xyzw;


r10.xy = cmp(v2.xx >= float2(0.5,0.100000001));
r10.xy = step(v2.xx ,  float2(0.5,0.100000001))-1;;

(r[\s\S]*)= cmp\(([\s\S]*) [=]*>[=]* ([\s\S]*)\);
$1 = step($2 , $3)-1;

(r[\s\S]*)= cmp\(([\s\S]*) [=]*<[=]* ([\s\S]*)\);
$1 = step($3 , $2)-1;




step\((.*),.*0 ,
step($1,