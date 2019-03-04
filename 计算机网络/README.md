# 通过一次完整的 HTTP 请求串起整个计算机网络

一直感觉网上给的计算机网络的整理文章中的知识点都非常的零散，而人类对于零散知识的记忆能力是有限的，但其实计算机网络本身是很有逻辑的。所以，本文将通过一次完整的 HTTP 请求将计算机网络的常见知识点串起来，即从在浏览器中输入 URL 地址开始，讲到浏览器显示主页，其中涉及到的知识的详细介绍，将以链接的形式给出，想要详细了解一下哪部分知识，只要点进去看一下就好啦，这样不会影响到我们对整体内容的把握。先假设我们要访问 www.baidu.com 吧！（因为据说百度超喜欢问这个……）

首先，想要访问百度，我们需要在浏览器的地址栏中输入 www.baidu.com，这是一个 [URL](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#url-%E5%92%8C-uri)，输入 URL 点击回车之后，我们的请求就发出去了，然后我们只需等待服务器响应我们的请求，返回我们请求的数据，在通过浏览器对返回的数据进行渲染，就得到了我们看到的页面。总体来说分为以下几个过程：

1. DNS 解析
2. TCP 连接
3. 发送 HTTP 请求
4. 服务器处理请求并返回 HTTP 报文
5. 浏览器解析渲染页面，显示主页

最后 1 个过程其实和计算机网络没啥关系了，所以我们主要研究前 4 个过程。

首先是 [DNS 解析](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#dns-%E8%A7%A3%E6%9E%90-1)，DNS 解析的过程就是寻找哪台机器上有你需要资源的过程。当然目前国内访问量较高的网站的架构不会如此的简单，它们会使用 [CDN 网络加速技术](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#cdncontent-distribute-network)。反正最终的目的都只有一个，就是将我们输入的 URL 地址转换为 IP 地址。

得到目标的 IP 地址之后，我们就要向他请求主页了，请求从我们的电脑到达服务器的流程主要如下图所示：

![浏览器发送请求到服务器的过程.jpg](./pic/浏览器发送请求到服务器的过程.jpg)

我们的请求始于应用层，会先构成一个 HTTP 请求报文，然后将这个报文传到传输层，传输层的 TCP 协议会将 HTTP 报文切成大小合适的块块，每一块加上一个 TCP 头，打包成一个 TCP 报文，在把它们传到网络层，网络层采用的是 IP 协议，IP 协议会再次对数据进行包装，加上一个 IP 头，然后数据就要开始真正的在物理链路上进行传输了，IP 协议会搜索对方的地址，一边中转一边将数据传送给目标服务器。根据 IP 地址找到服务器后，再经过一次以上过程的逆过程，服务器最终会收到我们的请求。

对于 HTTP 协议，我们有以下零散的知识点需要掌握一下：

- [HTTP 长连接、短连接？](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#http-%E9%95%BF%E8%BF%9E%E6%8E%A5%E7%9F%AD%E8%BF%9E%E6%8E%A5)
- [HTTP 1.1 与 HTTP 1.0 的区别？](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#http-11-%E4%B8%8E-http-10-%E7%9A%84%E5%8C%BA%E5%88%AB)
- [HTTP、HTTPS 区别？](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#httphttps-%E5%8C%BA%E5%88%AB)

接下来是 TCP 协议，TCP 是一种面向连接、确保数据在端到端间可靠传输的协议。它在传输前是需要先建立一条可靠的传输链路的，然后让数据在这条链路上流动，完成传输。简单来说就是，TCP 在想尽各种办法保证数据传输的可靠性，为了可靠性 TCP 会这样进行数据传输：（TCP 的传输方式与 [TCP 报头](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#tcp-%E6%8A%A5%E5%A4%B4%E7%BB%93%E6%9E%84)中的一些字段息息相关，最好先了解一下）

- [三次握手建立连接](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E4%B8%89%E6%AC%A1%E6%8F%A1%E6%89%8B)；
- 对发出的每一个字节进行编号确认，校验每一个数据包的有效性，在出现超时进行重传；
- 通过[流量控制](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6)（通过[滑动窗口协议](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E4%BB%80%E4%B9%88%E6%98%AF-tcp-%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)实现）和[拥塞控制](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E6%8B%A5%E5%A1%9E%E6%8E%A7%E5%88%B6)（[慢启动和拥塞避免](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E6%85%A2%E5%90%AF%E5%8A%A8%E5%92%8C%E6%8B%A5%E5%A1%9E%E9%81%BF%E5%85%8D)、[快重传和快恢复](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E5%BF%AB%E9%87%8D%E4%BC%A0%E5%92%8C%E5%BF%AB%E6%81%A2%E5%A4%8D)）等机制，避免网络状况恶化而影响数据传输；
- [四次挥手断开连接](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E5%9B%9B%E6%AC%A1%E6%8C%A5%E6%89%8B)。

> 补充 1：传输层不只有个 TCP 协议，还有一个 UDP 协议也很常见，它们的区别为：[TCP 与 UDP 的区别？](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#tcp-%E4%B8%8E-udp-%E7%9A%84%E5%8C%BA%E5%88%AB)

> 补充 2：[如果客户端不断的发送请求连接会怎样？](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E5%A6%82%E6%9E%9C%E5%AE%A2%E6%88%B7%E7%AB%AF%E4%B8%8D%E6%96%AD%E7%9A%84%E5%8F%91%E9%80%81%E8%AF%B7%E6%B1%82%E8%BF%9E%E6%8E%A5%E4%BC%9A%E6%80%8E%E6%A0%B7)
>
> 答：会发生 DDos 攻击，这个攻击的产生原因与 TCP 连接建立的三次握手息息相关。

收到请求的服务器会对请求进行处理，并将结果包装成一个 HTTP 应答报文，经过以上过程的逆过程，返回给客户端。

HTTP 应答报文有个叫状态码的东西，这个有好多，以下列出几个常见的：

- 100：请求者继续提出请求
- 200：请求成功
- [301 & 302：重定向](https://github.com/TangBean/MarkdownNotes/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C.md#%E4%BB%80%E4%B9%88%E6%98%AF-301302-%E9%87%8D%E5%AE%9A%E5%90%91)
- 4xx：请求错误（客户端的问题）
- 5xx：服务器错误

最后，浏览器渲染一下服务器返回的主页数据，我们就可以在浏览器上看到百度的搜索页面了。