the code template:

int f[1000];  //the union-find set


void init(int n) {    //init itself as its father node
    for(int i = 0; i < n; i++) {
        f[i] = i;
    }
}
//finding the father node（use path flattening）
int find(int a) {
 if(f[a] != a) {  // the value isn't itself,so it has the father, at the same time, set its father as its father's father
    f[a] = find(f[a]);
 }

 return f[a];   //the last father node
}

//is same father node
bool isSameSet(int a,int b) {
    return find(a) == find(b);
}

//union the different father when they has different father node(not union by size)
void unite(int a,int b) {
    int fx = find(a);
    int fy = find(b);

    if(fx != fy) {
        f[fx] = fy;
    }
}

