设计模式

1、桥接设计模式

解决的问题：当有多个独立变化的维度被绑定时会造成类创建爆炸的问题，代码耦合度高


******例子：比如设计手机 + 系统的案例******


***未进行桥接模式的设计代码***
abstract class Phone {
    // 抽象方法：开机
    public abstract void boot();
}
// 华为 + 鸿蒙 
class HuaweiHarmony extends Phone{
    @Override
    public void boot() {
        System.out.println("华为手机 运行 鸿蒙系统");
    }
}

// 华为 + 安卓 
class HuaweiAndroid extends Phone{
    @Override
    public void boot() {
        System.out.println("华为手机 运行 安卓系统");
    }
}

// 小米 + 鸿蒙 
class XiaoMiHarmony extends Phone{
    @Override
  public void boot() {
        System.out.println("小米手机 运行 鸿蒙系统");
    }
}
发现的问题是如果要写m个手机品牌加n个系统创建类的数量就是 m × n


***桥接设计模式的代码***
interface OS {
    void run();
}

class Android implements OS {
    @Override
    public void run() {
        System.out.println("运行安卓系统");
    }
}

class Harmony implements OS {
    @Override
    public void run() {
        System.out.println("运行鸿蒙系统");
    }
}
abstract class Phone {
    protected OS os;

    public Phone(OS os) {
        this.os = os;
    }

    public abstract void boot();
}
class Huawei extends Phone {
    public Huawei(OS os) {
        super(os);
    }

    @Override
    public void boot() {
        System.out.print("华为手机：");
        os.run();
    }
}

class XiaoMi extends Phone {
    public XiaoMi(OS os) {
        super(os);
    }

    @Override
    public void boot() {
        System.out.print("小米手机：");
        os.run();
    }
}
在此设计模式下会将创建类的数量优化到 m + n


***设计过程***
1、识别出两个独立变化的维度（  此用例为：系统（附属维度），手机品牌（主体维度））
将两个独立维度一个为主体维度（不会随意更换的骨架），另一个为附属维度（配件，可随意替换搭配）
2、给附属维度定义为接口 + 具体实现
//接口
interface OS{
    void run();
}
//具体实现
// 安卓系统
class Android implements OS{
    @Override
    public void run() {
        System.out.println("运行安卓系统");
    }
}

// 鸿蒙系统
class Harmony implements OS{
    @Override
    public void run() {
        System.out.println("运行鸿蒙系统");
    }
}
3、将主体维度定义为抽象类并将系统作为属性
//手机抽象类
abstract class Phone {
    protected OS os;  // 桥：把系统抽出来当属性

    public Phone(OS os){
        this.os = os;
    }
    public abstract void boot();
}
