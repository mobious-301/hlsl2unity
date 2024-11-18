linux shell:
dot -Tpdf D:\MLearning\tree.dot -o D:\MLearning\tree.pdf 



r6.xyzw = t1.SampleBias(s1_s, v3.xy, cb0[133].x).xyzw;
(r[\s\S]*)= ([\s\S]*).SampleBias\([\s\S]*s, ([\s\S]*), [\s\S]*\).([\s\S]*);
$1 = tex2D($2,$3).$4;



r10.xy = cmp(v2.xx >= float2(0.5,0.100000001));
r10.xy = step(v2.xx ,  float2(0.5,0.100000001))-1;;

(r[\s\S]*)= cmp\(([\s\S]*) [=]*>[=]* ([\s\S]*)\);
$1 = step($2 , $3)-1;

(r[\s\S]*)= cmp\(([\s\S]*) [=]*<[=]* ([\s\S]*)\);
$1 = step($3 , $2)-1;
