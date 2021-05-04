---
title: 物理层
date: 2021-04-22 22:22:00.631
updated: 2021-04-22 22:24:39.061
url: http://blog.halo123.top:8090/archives/物理层
categories: 计算机网络
tags: 计算机网络
---

## 物理层的基本概念

物理层解决如何在连接各种计算机的传输媒体上<font color="#FF666">传输数据比特流</font>，而不是指具体的传输媒体。

物理层主要任务:确定与传输媒体<font color="#faa755">接口</font>有关的一些特性(定义标准)

1. 机械特性:定义物理连接的特性，规定物理连接时所采用的规格、接口形状、<font color="#faa755">引线数目</font>、<font color="#faa755">引脚数量</font>和排列情况。

2. 电气特性:规定传输二进制位时，线路上信号的<font color="#faa755">电压范围</font>、阻抗匹配、传输<font color="#faa755">速率</font>和<font color="#faa755">距离</font>限制等。

   > 某网络在物理层规定，信号的电平用+10V~+15V表示二进制0，用-10V~-15V表示二进制1，电线长度限于15m以内

3. 功能特性:指明某条线上出现的某一<font color="#faa755">电平表示何种意义</font>，接口部件的信号线的用途。

   > 描述一个物理层接口引脚处于高电平时的含义时

4. 规程特性:(过程特性) 定义各条物理线路的工作<font color="#faa755">规程和时序</font>关系。

# 通信基础

## 1 基本概念

<img src="https://halo-blog-img.oss-cn-hangzhou.aliyuncs.com/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E5%85%B8%E5%9E%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%80%9A%E4%BF%A1%E6%A8%A1%E5%9E%8B.png" alt="典型的数据通信模型" style="object-fit: cover; border-radius: 10px; width: 100%;" />

通信的目的是<font color="#faa755">传送信息</font>。

<font color="#ea66a6">数据</font>:传送信息的实体，通常是有意义的符号序列。

<font color="#ea66a6">信号</font>:数据的电气或电磁的表现，是数据在传输过程中的<font color="#faa755">存在形式</font>。

+ 数字信号:代表消息的参数取值是离散的。取值仅允许为有限的几个离散数值的数据(或信号)称为数字数据(或数字信号)。
+ 模拟信号:代表消息的参数取值是连续的。连续变化的数据(或信号)称为模拟数据(或模拟信号);

<font color="#ea66a6">信源</font>:产生和发送数据的源头。

<font color="#ea66a6">信宿</font>:接收数据的终点。

<font color="#ea66a6">信道</font>:信号的传输媒介。一般用来表示向某一个方向传送信息的介质，因此一条通信线路往往包含一条发送信道和一条接收信道。

+ 信道按传输<font color="#ef5b9c">信号形式</font>的不同可分为传送模拟信号的<font color="#faa755">模拟信道</font>和传送数字信号的<font color="#faa755">数字信道</font>两大类;

+ 信道按传输<font color="#ef5b9c">介质</font>的不同可分为<font color="#faa755">无线信道</font>和<font color="#faa755">有线信道</font>。

从通信双方信息的交互方式看，可分为三种基本方式:

1. <font color="#ea66a6">单工通信</font>。只有一个方向的通信而没有反方向的交互，仅需要<font color="#FF666">一条</font>信道。例如，无线电广播、电视广播就属于这种类型。
2. <font color="#ea66a6">半双工通信</font>。通信的双方都可以发送或接收信息，但任何一方都<font color="#faa755">不能同时</font>发送和接收信息，此时需要<font color="#FF666">两条</font>信道。(对讲机)
3. <font color="#ea66a6">全双工通信</font>。通信双方可以同时发送和接收信息，也需要<font color="#FF666">两条</font>信道。

数据传输方式可分为串行传输和并行传输。

+ <font color="#ea66a6">串行传输</font>是指一个一个的比特按照时间顺序传输(出于经济上的考虑，远距离通信通常采用串行传输)
+ <font color="#ea66a6">并行传输</font>是指多个比特通过多条通信信道同时传输。

---

<font color="#ea66a6">码元</font>是指用一个<font color="#FF666">固定时长</font>的<font color="#FF666">信号波形</font>(数字脉冲)表示一位k进制数字，代表不同离散数值的基本波形，是数字通信中数字信号的计量单位，这个时长内的信号称为<font color="#ea66a6">k进制码元</font>，而该时长称为<font color="#ea66a6">码元宽度</font>。1码元可以携带多个比特的信息量。例如，在使用二进制编码时，只有两种不同的码元: 一种代表0状态，另一种代表1状态。

速率也称数据率，指的是数据的<font color="#FF666">传输速率</font>，表示单位时间内传输的数据量。可以用<font color="#faa755">码元传输速率</font>和<font color="#faa755">信息传输速率</font>表示。

+ <font color="#ea66a6">码元传输速率</font>。又称码元速率、波形速率、调制速率、符号速率等，它表示单位时间内数字通信系统所传输的码元个数(也可称为<font color="#faa755">脉冲个数或信号变化的次数</font>)，单位是<font color="#FF666">波特</font>(Baud)。 1波特表示数字通信系统每秒传输一个码元。这里的码元可以是多进制的，也可以是二进制的，但码元速率与进制数无关。<font color="#FF666">1s传输多少个码元</font>
+ <font color="#ea66a6">信息传输速率</font>。又称信息速率、比特率等，它表示单位时间内数字通信系统传输的二进制码元个数(即比特数)，单位是比特/秒(b/s)。<font color="#FF666">1s传输多少个比特</font>

> 关系:<font color="#faa755">若一个码元携带n比特的信息量，则M波特率的码元传输速率所对应的信息传输速率为M×n bit/s</font>。

<font color="#ea66a6">带宽</font>:表示在单位时间内从网络中的某一点到另一点所能通过的“<font color="#faa755">最高数据率</font>”，常用来表示网络的通信线路所能传输数据的能力。单位是b/s。

## <font color="#d9730d">2 奈奎斯特定理与香农定理</font>

影响失真程度的影响因素:

1. 码元传输速率,速率越快失真越严重
2. 信号传输距离,距离越远失真越严重
3. 噪声干扰,干扰越多失真越严重
4. 传输媒体质量,质量越差失真越严重

具体的信道所能通过的频率范围总是有限的(信道带宽).信号中的许多高频分量往往不能通过信道,否则在传输中会衰减,导致接收端收到的信号波形<font color="#faa755">失去码元之间清晰界限</font>,这种现象称为<font color="#ea66a6">码间串扰</font>

<font color="#ea66a6">信道带宽</font>:是信道能通过的最高频率和最低频率之差.

### 奈奎斯特定理

奈奎斯特(Nyquist)定理又称<font color="#ea66a6">奈氏准则</font>，它指出在理想低通(没有噪声、带宽有限)的信道中，极限码元传输率为2W波特，其中<font color="#faa755">W</font>是理想低通信道的带宽，单位为<font color="#FF666">Hz</font>。若用<font color="#faa755">V</font>表示每个码元离散电平的数目(码元的离散电平数目是指有多少种不同的码元，比如有16种不同的码元，则需要4位二进制位，因此数据传输率是码元传输率的4倍)，则极限数据率为

理想低通信道下的极限数据传输率= 2W log<sub>2</sub>V (单位为b/s)

对于奈氏准则，可以得出以下结论:

1. 在任何信道中，码元传输的速率是有上限的。若传输速率超过此上限，就会出现严重的码间串扰问题(指在接收端收到的信号波形失去了码元之间的清晰界限)，使得接收端不可能完全正确识别码元。
2. 信道的频带越宽(即通过的信号高频分量越多)，就可用更高的速率进行码元的有效传输。
3. 奈氏准则给出了码元传输速率的限制，但并未对信息传输速率给出限制，即未对一个码元可以对应多少个二进制位给出限制。

由于码元的传输速率受奈氏准则的制约，所以要提高数据的传输速率，就必须设法使每个码元携带更多个比特的信息量，此时就需要采用多元制的调制方法。

### 香农定理

<font color="#ea66a6">噪声</font>存在于所有的电子设备和通信信道中。由于噪声随机产生，它的瞬时值有时会很大，因此噪声会使接收端对码元的判决产生错误。但是噪声的影响是相对的，若信号较强，那么噪声影响相对较小。因此，<font color="#ea66a6">信噪比</font>就很重要。

香农(Shannon)定理给出了带宽受限且有高斯白噪声干扰的信道的极限数据传输率，当用此速率进行传输时，可以做到不产生误差。香农定理定义为

<font color="#faa755">信道的极限数据传输率 = Wlog<sub>2</sub>(1+S/N) (单位为b/s)</font>

式中，W为信道的带宽，S为信道所传输信号的平均功率，N为信道内部的高斯噪声功率。S/N为信噪比，即信号的平均功率与噪声的平均功率之比，<font color="#FF666">信噪比 = 10log<sub>10</sub>(S/N) (单位为dB)</font>，例如如当S/N= 10时，信噪比为10dB，而当S/N= 1000时，信噪比为30dB。

对于香农定理，可以得出以下结论:

1. 信道的带宽或信道中的信噪比越大，信息的极限传输速率越高。
2. 对一定的传输带宽和一定的信噪比，信息传输速率的上限是确定的。
3. 只要信息的传输速率低于信道的极限传输速率，就能找到某种方法来实现无差错的传输。
4. 香农定理得出的是极限信息传输速率，实际信道能达到的传输速率要比它低不少。

从香农定理可以看出，若信道带宽W或信噪比SIN没有上限(实际信道当然不可能这样)，则信道的极限信息传输速率也没有上限。

奈氏准则只考虑了带宽与极限码元传输速率的关系，而香农定理不仅考虑到了带宽，也考虑到了信噪比。这从另一个侧面表明，一个码元对应的二进制位数是有限的。

## 3 编码与调制

信道上传送信号的两种形式:基带信号和宽带信号

+ 基带信号:将数字信号1和0直接用两种不同的电压表示，再送到<font color="#faa755">数字信道</font>上去传输(<font color="#faa755">基带传输</font>)

  > <font color="#ef5b9c">来自信源的信号</font>，像计算机输出的代表各种文字或图像文件的数据信号都属于基带信号。基带信号就是发出的直接表达了要传输的信息的信号，比如我们说话的声波就是基带信号。

+ 宽带信号:将基带信号进行调制后形成的频分复用模拟信号，再传送到<font color="#faa755">模拟信道</font>上去传输(<font color="#faa755">宽带传输</font>)

  > 把基带信号经过载波调制后，把信号的频率范围搬移到较高的频段以便在信道中传输(即仅在一段频率范围内能够通过信道)。

在传输距离较<font color="#faa755">近</font>时，计算机网络采用<font color="#ef5b9c">基带传输</font>方式(近距离衰减小，从而信号内容不易发生变化)

在传输距离较<font color="#faa755">远</font>时，计算机网络采用<font color="#ef5b9c">宽带传输</font>方式(远距离衰减大，即使信号变化大也能最后过滤出来基带信号)

### 数字数据编码为数字信号

数字数据编码用于基带传输中，即在基本不改变数字数据信号频率的情况下，直接传输数字信号。具体用什么样的数字信号表示0及用什么样的数字信号表示1就是所谓的编码。编码的规则有多种，只要能有效地把1和0区分开即可，常用的编码方式有以下几种，如下图所示。

<img src="https://halo-blog-img.oss-cn-hangzhou.aliyuncs.com/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E5%B8%B8%E7%94%A8%E7%9A%84%E6%95%B0%E5%AD%97%E6%95%B0%E6%8D%AE%E7%BC%96%E7%A0%81%E6%96%B9%E5%BC%8F.png" alt="常用的数字数据编码方式" style="object-fit: cover; border-radius: 10px; width: 80%;" />

1. 归零编码(RZ)

   在归零编码中用高电平代表1、低电平代表0 (或者相反)，每个时钟周期的中间均跳变到低电平(归零)，接收方根据该跳变调整本方的时钟基准，这就为传输双方提供了自同步机制。由于归零需要占用一部分带宽，因此传输效率受到了一定的影响。

2. 非归零编码(NRZ)

   非归零编码与RZ编码的区别是不用归零,一个周期可以全部用来传输数据。但NRZ编码无法传递时钟信号，双方难以同步，因此若想传输高速同步数据，则需要都带有时钟线。

3. 反向非归零编码(NRZI)

   反向非归零码与NRZ编码的区别是用信号的翻转代表0、信号保持不变代表1。翻转的信号本身可以作为一种通知机制。这种编码方式集成了前两种编码的优点，既能传输时钟信号，又能尽量不损失系统带宽。USB2.0通信的编码方式就是NRZI编码。

4. 曼彻斯特编码(Manchester Encoding)

   曼彻斯特编码将一个码元分成两个相等的间隔，前一个间隔为高电平而后一个间隔为低电平表示码元1;码元0的表示方法则正好相反。当然，也可采用相反的规定。该编码的特点是，在每个码元的中间出现电平跳变，位中间的跳变既作为时钟信号(可用于同步)，又作为数据信号，但它所占的频带宽度是原始基带宽度的两倍。<font color="#faa755">以太网使用的编码方式就是曼彻斯特编码</font>。

5. 差分曼彻斯特编码

   差分曼彻斯特编码常用于局域网传输,其规则是,若码元为1,则前半个码元的电平与上一个码元的后半个码元的电平相同;若码元为0，则情形相反。该编码的特点是，在每个码元的中间都有一次电平的跳转，可以实现自同步，且<font color="#faa755">抗干扰性较好</font>。

6. 4B/5B编码

   将欲发送数据流的每4位作为一组，然后按照4B/5B编码规则将其转换成相应的5位码。5位码共32种组合，但只采用其中的16种对应16种不同的4位码，其他的16种作为控制码(帧的开始和结束、线路的状态信息等)或保留。

### 数字数据调制为模拟信号

数字数据调制技术在发送端将数字信号转换为模拟信号,而在接收端将模拟信号还原为数字信号，分别对应于调制解调器的调制和解调过程。基本的调制方法有如下几种:

1. 幅移键控(ASK)。通过改变载波信号的振幅来表示数字信号1和0，而载波的频率和相位都不改变。比较容易实现，但抗干扰能力差。调幅(AM)
2. 频移键控(FSK)。 通过改变载波信号的频率来表示数字信号1和0，而载波的振幅和相位都不改变。容易实现，抗干扰能力强，目前应用较为广泛。调频(FM)
3. 相移键控(PSK)。 通过改变载波信号的相位来表示数字信号1和0，而载波的振幅和频率都不改变。它又分为绝对调相和相对调相。调相
4. 正交振幅调制(QAM)。在频率相同的前提下，将ASK与PSK结合起来，形成叠加信号。设波特率为B,采用m个相位，每个相位有n种振幅，则该QAM技术的数据传输率R为:R= Blog<sub>2</sub>(mn) (单位为b/s).调幅+调相

<img src="https://halo-blog-img.oss-cn-hangzhou.aliyuncs.com/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E6%95%B0%E5%AD%97%E8%B0%83%E5%88%B6%E7%9A%84%E4%B8%89%E7%A7%8D%E6%96%B9%E5%BC%8F.png" alt="数字调制的三种方式" style="object-fit: cover; border-radius: 10px; width: 900%;" />

### 模拟数据编码为数字信号

这种编码方式最典型的例子是常用于对音频信号进行编码的<font color="#ea66a6">脉码调制(PCM)</font>。它主要包括三个步骤，即采样、量化和编码。

<font color="#ea66a6">采样定理</font>:在通信领域，带宽是指信号最高频率与最低频率之差，单位为Hz。因此，将模拟信号转换成数字信号时，假设原始信号中 的最大频率为$f$,那么采样频率$f_{采样}$必须大于等于最大频率$f$的两倍，才能保证采样后的数字信号完整保留原始模拟信号的信息(只需记住结论)。另外，采样定理又称奈奎斯特定理。

1. <font color="#ea66a6">采样</font>:是指对模拟信号进行周期性扫描，把时间上连续的信号变成时间上离散的信号。根据采样定理，当采样的频率大于等于模拟数据的频带带宽(最高变化频率)的两倍时，所得的离散信号可以无失真地代表被采样的模拟数据。
2. <font color="#ea66a6">量化</font>:是把采样取得的电平幅值按照一定的分级标度转化为对应的数字值并取整数，这样就把连续的电平幅值转换为了离散的数字量。采样和量化的实质就是分割和转换。
3. <font color="#ea66a6">编码</font>:是把量化的结果转换为与之对应的二进制编码。

### 模拟数据调制为模拟信号

为了实现传输的有效性，可能需要较高的频率。这种调制方式还可以使用频分复用(FDM)技术，充分利用带宽资源。电话机和本地局交换机采用模拟信号传输模拟数据的编码方式;模拟的声音数据是加载到模拟的载波信号中传输的。

### 4 电路交换、报文交换与分组交换

P40

# 传输介质

<font color="#ea66a6">传输介质</font>也称传输媒体，它是发送设备和接收设备之间的<font color="#faa755">物理通路</font>。

> <font color="#faa755">传输媒体并不是物理层</font>。传输媒体在物理层的下面，因为物理层是体系结构的第一层， 因此有时称传输媒体为0层。在传输媒体中传输的是信号，但传输媒体并不知道所传输的信号代表什么意思。但物理层规定了电气特性，因此能够识别所传送的比特流。

传输介质可分为导向传输介质和非导向传输介质。

+ <font color="#ea66a6">导向传输介质</font>中，电磁波被导向沿着固体媒介(铜线或光纤)传播
+ <font color="#ea66a6">非导向传输介质</font>可以是空气、真空或海水等

## 双绞线、同轴电缆、光纤与无线传输介质

### 双绞线

双绞线是最常用的古老传输介质,它由两根采用一定规则并排绞合的、相互绝缘的铜导线组成。<font color="#faa755">绞合可以减少对相邻导线的电磁干扰</font>。

为了进一步提高抗电磁干扰能力，可在双绞线的外面再加上一个由<font color="#faa755">金属丝</font>编织成的屏蔽层，这就是屏蔽双绞线(STP)。无屏蔽层的双绞线称为非屏蔽双绞线(UTP)。 

它们的结构如图下所示。

<img src="https://halo-blog-img.oss-cn-hangzhou.aliyuncs.com/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E5%8F%8C%E7%BB%9E%E7%BA%BF%E7%9A%84%E7%BB%93%E6%9E%84.png" alt="双绞线的结构" style="object-fit: cover; border-radius: 10px; width: 100%;" />

双绞线价格便宜，是最常用的传输介质之一，在局域网和传统电话网中普遍使用。

双绞线的带宽取决于铜线的粗细和传输的距离。

模拟传输和数字传输都可使用双绞线，其通信距离一般为几千米到数十千米。

距离太远时，对于<font color="#ef5b9c">模拟传输</font>，要用<font color="#ef5b9c">放大器</font>放大衰减的信号;对于<font color="#faa755">数字传输</font>，要用<font color="#faa755">中继器</font>将失真的信号整形。

### 同轴电缆

同轴电缆由内导体、绝缘层、网状编织屏蔽层和塑料外层构成，如下图所示。

<img src="https://halo-blog-img.oss-cn-hangzhou.aliyuncs.com/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E5%90%8C%E8%BD%B4%E7%94%B5%E7%BC%86%E7%9A%84%E7%BB%93%E6%9E%84.png" alt="同轴电缆的结构" style="object-fit: cover; border-radius: 10px; width: 80%;" />

按特性阻抗数值的不同，通常将同轴电缆分为两类: 50Ω同轴电缆和75Ω同轴电缆。

+ 50Ω同轴电缆主要用于传送基带数字信号，又称<font color="#ea66a6">基带同轴电缆</font>，它在局域网中应用广泛; 
+ 75Ω同轴电缆主要用于传送宽带信号，又称<font color="#ea66a6">宽带同轴电缆</font>，主要用于有线电视系统。

由于外导体屏蔽层的作用，同轴电缆具有良好的抗干扰特性，被广泛用于传输较高速率的数据，其传输距离更远，但价格较双绞线贵。

### 光纤

光纤通信就是利用光导纤维(简称光纤)传递光脉冲来进行通信。有光脉冲表示1，无光脉冲表示0。可见光的频率约为10<sup>8</sup>MHz，因此光纤通信系统的带宽范围极大。

光纤在发送端有光源，可以采用发光二极管或半导体激光器，它们在电脉冲作用下能产生出光脉冲;在接收端用光电二极管做成光检测器，在检测到光脉冲时可还原出电脉冲。

光纤主要由<font color="#faa755">纤心</font>和<font color="#faa755">包层</font>构成，光波通过纤心进行传导，包层较纤心有较低的折射率。当光线从高折射率的介质射向低折射率的介质时，其折射角大于入射角。因此，如果入射角足够大，那么就会出现全反射，即光线碰到包层时会折射回纤心，这个过程不断重复，光也就沿着光纤传输下去。

<img src="https://halo-blog-img.oss-cn-hangzhou.aliyuncs.com/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E5%85%89%E6%B3%A2%E5%9C%A8%E7%BA%A4%E5%BF%83%E4%B8%AD%E7%9A%84%E4%BC%A0%E6%92%AD.png" alt="光波在纤心中的传播" style="object-fit: cover; border-radius: 10px; width: 100%;" />

只要从纤心中射到纤心表面的光线的入射角大于某个临界角度，就会产生全反射。因此，从不同角，度入射的多束光线可在一条光纤中传输， 这种光纤称为<font color="#ea66a6">多模光纤</font>，多模光纤的光源为<font color="#faa755">发光二极管</font>。光脉冲在多模光纤中传输时会逐渐展宽，造成失真，因此多模光纤只适合于<font color="#faa755">近距离传输</font>。

<img src="https://halo-blog-img.oss-cn-hangzhou.aliyuncs.com/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E5%A4%9A%E6%A8%A1%E5%85%89%E7%BA%A4.png" alt="多模光纤" style="object-fit: cover; border-radius: 10px; width: 100%;" />

光纤的直径减小到仅一个光波长度时，光纤就像一根波导 那样，可使光线一直向前传播， 而不会产生多次反射，这样的光纤就是单模光纤。 单模光纤的纤心很细，直径只有几微米，制造成本较高。同时，单模光纤的光源为<font color="#faa755">定向性很好的激光二极管</font>，因此单模光纤的衰减较小，适合<font color="#faa755">远距离传输</font>。

光纤的特点:

1. 传输损耗小，中继距离长，对远距离传输特别经济。
2. 抗雷电和电磁干扰性能好。
3. 无串音干扰，保密性好，也不易被窃听或截取数据。
4. 体积小，重量轻。

### 无线传输介质（非导向传播介质）

无线通信已广泛应用于移动电话领域，构成蜂窝式无线电话网。随着便携式计算机的出现，以及在军事、野外等特殊场合下移动通信联网的需要，促进了数字化移动通信的发展，现在无线局域网产品的应用已非常普遍。

#### 无线电波

无线电波具有<font color="#faa755">较强的穿透能力</font>，可以传输很长的距离，所以它被广泛应用于通信领域，如无线手机通信、计算机网络中的无线局域网(WLAN)等。因为无线电波使信号向所有方向散播,因此有效距离范围内的接收设备无须对准某个方向，就可与无线电波发射者进行通信连接，大大简化了通信连接。这也是无线电传输的最重要优点之一。

#### 微波、红外线和激光

目前高带宽的无线通信主要使用三种技术:微波、红外线和激光。它们都需要发送方和接收方之间存在一条视线(Line-of-sight) 通路，有很强的方向性，都沿直线传播，有时统称这三者为视线介质。不同的是，红外通信和激光通信把要传输的信号分别转换为各自的信号格式，即红外光信号和激光信号，再直接在空间中传播。

微波通信的频率较高，频段范围也很宽，载波频率通常为2~40GHz,因而通信信道的容量大。例如，一个带宽为2MHz的频段可容纳500条语音线路，若用来传输数字信号，数据率可达数兆比特/秒。与通常的无线电波不同，微波通信的信号是沿直线传播的，因此在地面的传播距离有限，超过一定距离后就要用中继站来接力。

卫星通信利用地球同步卫星作为中继来转发微波信号，可以克服地面微波通信距离的限制。三颗相隔120°的同步卫星几乎能覆盖整个地球表面，因而基本能实现全球通信。卫星通信的优点是通信容量大、距离远、覆盖广、广播通信和多址通信，缺点是端到端传播时延长，一般为 250~270ms、受气候影响大（强风、太阳黑子爆发、日凌）、误码率较高、成本高。

# 物理层设备

## 中继器

诞生原因:由于存在损耗，在线路上传输的信号功率会逐渐衰减，衰减到一定程度时将造成信号失真，因此会导致接收错误。

中继器的功能:对信号进行<font color="#faa755">再生和还原</font>，对衰减的信号进行放大，保持与原数据相同，以增加信号传输的距离，延长网络的长度。<font color="#FF666">再生数字信号</font>

中继器的两端:

+ 两端的网络部分是网段，而不是子网，适用于完全相同的两类网络的互连，且两个网段速率要相同。
+ 中继器只将任何电缆段上的数据发送到另一段电缆上，它仅作用于信号的电气部分，并不管数据中是否有错误数据或不适于网段的数据。
+ 两端可连相同媒体，也可连不同媒体。
+ 中继器两端的网段一定要是同一个协议。

中继器又称转发器，主要功能是将信号整形并放大再转发出去，以消除信号经过一长段电缆后，因噪声或其他原因而造成的失真和衰减，使信号的波形和强度达到所需要的要求，进而扩大网络传输的距离。其原理是信号再生(而非简单地将衰减的信号放大)。中继器有两个端口，数据从一个端口输入，再从另一个端口发出。端口仅作用于信号的电气部分，而不管数据中是否有错误数据或不适于网段的数据。

中继器是局域网环境下用来扩大网络规模的最简单、最廉价的互联设备。使用中继器连接的几个网段仍然是一个局域网。一般情况下，中继器的两端连接的是相同的媒体，但有的中继器也可以完成不同媒体的转接工作。但由于中继器工作在物理层，因此它不能连接两个具有不同速率的局域网。中继器两端的网络部分是网段，而不是子网。中继器若出现故障，对相邻两个网段的工作都将产生影响。

从理论上讲，中继器的使用数目是无限的，网络因而也可以无限延长。但事实上这不可能,因为网络标准中对信号的延迟范围做了具体的规定，<font color="#faa755">中继器只能在此规定范围内进行有效的工作，否则会引起网络故障</font>。例如，在采用粗同轴电缆的10BASE5 以太网规范中，互相串联的中继器的个数不能超过4个，而且用4个中继器串联的5段通信介质中只有3段可以挂接计算机，其余两段只能用作扩展通信范围的链路段，不能挂接计算机。这就是所谓的“<font color="#faa755">5-4-3规则</font>”。

> 注意:放大器和中继器都起放大作用，只不过放大器放大的是模拟信号,原理是将衰减的信号放大，而中继器放大的是数字信号，原理是将衰减的信号整形再生。如果某个网络设备具有存储转发的功能，那么可以认为它能连接两个不同的协议，如果该网络设备没有存储转发功能，那么认为它不能连接两个不同的协议。中继器是没有存储转发功能的，因此它不能连接两个速率不同的网段，中继器两端的网段一定要使用同一个协议。

### 集线器(多口中继器)

集线器(Hub)实质上是一个多端口的中继器，它也工作在物理层。当Hub工作时，一个端口接收到数据信号后，由于信号在从端口到Hub的传输过程中已有衰减，所以Hub便将该信号进行整形放大，使之<font color="#faa755">再生(恢复)到发送时的状态</font>，紧接着转发到其他所有(除输入端口外)处于工作状态的端口。如果同时有两个或多个端口输入，那么输出时会发生冲突，致使这些数据都无效。从Hub的工作方式可以看出，它在网络中只起信号放大和转发作用，目的是扩大网络的传输范围，而<font color="#faa755">不具备信号的定向传送能力</font>，即信号传输的方向是固定的，是一个标准的共享式设备。

Hub主要使用双绞线组建共享网络，是从服务器连接到桌面的最经济方案。在交换式网络中，Hub直接与交换机相连，将交换机端口的数据送到桌面上。使用Hub组网灵活，它把所有结点的通信集中在以其为中心的结点上，对结点相连的工作站进行集中管理，不让出问题的工作站影响整个网络的正常运行，并且用户的加入和退出也很自由。

由Hub组成的网络是共享式网络，但逻辑上仍是一个总线网。Hub的每个端口连接的网络部分是同一个网络的不同网段，同时Hub也只能在半双工状态下工作，网络的吞吐率因而受到限制.

> 注意:多台计算机必须会发生同时通信的情形，因此集线器不能分割冲突域，所有集线器的端口都属于同一个冲突域。集线器在一个时钟周期中只能传输一组信息，如果一台集线器连接的机器数目较多，且多台机器经常需要同时通信，那么将导致信息碰撞，使得集线器的工作效率很差。比如，一个带宽为10Mb/s的集线器上连接了8台计算机，当这8台计算机同时工作时，每台计算机真正所拥有的带宽为10/8Mb/s = 1.25Mb/s.
