#String[]  grammar
***define***
String[] strs = new String[5];  //length = 5
String[] strs = {"a", "b", "c"};  //initialize with multiple strings
***get array length***
int n = strs.length;
***iterate over a String Array***
for(int i = 0; i < strs.length; i++) {
    System.out.println(strs[i]);
}

#String grammar
***assign a string***
String s = "hello";
***get the length of string***
int len = s.length();
***get the k-th character***
char c = s.charAt(k);
***compare if two strings are equal***
s.equals(t)  //s and t are string

#Math.random()  --- the range of return value is from 0(inclusive) to 1(exclusive)(double)
Math.random() -- [0,1)
Math.random() * v --[0,v)
(int)Math.randow() *v --[0,1,2···，v - 1)

#queue
public Queue<Integer> queue = new LinkedList<>();
queue.isEmpty();
queue.offer();  insert the element
queue.poll(); get and remove the value from the front of queue
queue.peek(); get the value from the front of queue without removing it
queue.size();

#define the queue using the array([left,right))
int left,int right
isEmpty() --> left == right;
offer() --> arr[right++] = value;
poll() --> int temp = arr[left++];
peek() --> int temp = arr[left];
size() --> int size = right - left;

# the circular queue
int left,int right,int size,int limit

poll -->size > 0
offer -->size < limit(the max length of array)

isEmpty() --> size == 0;
isFull() --> size == limit;
offer() --> queue[r] = value; r = r == limit - 1 ? 0 : (r + 1);
poll() --> l = l == limit - 1 ? 0 : (l + 1); 
front() --> queue[l]
rear() --> r == 0 : limit - 1 : r - 1;
size() --> size

#stack
public Stack<Interger> stack = new Stack<>();

stack.isEmpty();
stack.push();
stack.pop();
stack.peek();
stack.size();

#define the stack using array
int size

isEmpty() --> size == 0;
push() --> arr[size++] = temp;
pop() --> size--;
peek() -->arr[size - 1];
size() --> size;


