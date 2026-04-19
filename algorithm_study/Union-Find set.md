#the Union-Find set  //并查集

***Union-Find is an effcient data structure specialized for fast set merging and set membership queries;***  //快速合并和查找元素所在的集合

//the optimization 优化
//Union by size  小挂大（通过让长度小的集合挂在长的集合，来将查找的过程长度剪短）
//path flattening  //路径扁平化（将不同集合联合时直接搞成最终父节点，这样不用顺着节点一直找父节点）

Time complexity:O(1)

Application Scenarios  of Union-Find set：
1、Connected components counting  //统计连通块个数

the function:
1、void init();
2、int find(a)   
3、bool isSameSet(a,b)  
4、void union(a,b) 
