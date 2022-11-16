推荐使用由阿里云官方发布的Alibaba Cloud Linux 3，在全面兼容CentOS/RHEL生态的同时，与阿里云基础设施做了深度优化，为实例提供专项的性能和稳定性优化，并提供完善的生态支持，同时用户还可以免费享受阿里云提供的全生命周期服务保障。

| **分类** | **特性/软件** | **Alibaba Cloud Linux 3** | **Anolis OS 8** | **CenOS 7 ARM** |
| --- | --- | --- | --- | --- |
| **总体** | **总体差异** | 支持阿里云全系架构 / 新特性适配 / 问题修复 / 安全漏洞修复 / 专项为倚天构建大量优化和稳定性调优  | 基于Alinux3的云上实践，贡献到龙蜥开源社区 | CentOS 7有CentOS社区发布，未明确提供支持内容 |
|  |  |  |  |  |
| **生命周期** | 2031/4/30 | 2031/6/30 | CentOS 7 ARM版2021-11-30 EOL |  |
|  |  |  | CentOS 8 2021-12-31 EOL |  |
| **技术支持** | 阿里云供迁移、技术支持，SLA保障 | 龙蜥社区供技术支持 | 开源-无服务； |  |
|  |  |  | 阿里云镜像-部分支持 |  |
|  |  |  |  |  |
| **内核** | 内核 | kernel 5.10 | kernel 5.10 | 4.18.0 |
| &**编译器&工具链** |  |  |  |  |
| glibc | 2.32 | 2.28 | 2.17-325 |  |
| gcc编译器 | gcc-10 | gcc 8.3 | gcc-4.8.5 |  |
| python | python27, python36, python38 | 同Alinux3 | python2.7, tops-python2.7 |  |
| 其他动态语言 | OpenJDK 11, OpenJDK 8， Node.js（新增）， PHP>=7.2, Ruby>=2.6, Perl>=5.26, SWIG 3.0 | 同Alinux3 | php-5.x , ruby-2.5, perl-5.16 |  |
| 静态语言 | rust 1.45 到1.54 ， golang 1.12 到1.16 | 同Alinux3 | golang-1.4 |  |
| 软件包分发工具 | yum | yum | yum |  |
|  | dnf-4.4.2 ( 新增module方式支持多个基础软件譬如mysql等大版本切换） | dnf-4.4.2 |  |  |
| 时间服务 | chrony-4.1 | chrony-4.1 | ntp, chrony-3.4 |  |
| ARM | ARM兼容性 | Yitian710，Intel SPR，龙蜥生态硬件（龙芯等） | 同Alinux3 | 7.9开始兼容ARM，社区未成熟运行 |
| 芯片支持 |  |  |  | 建议8.4以上版本 |
| ARM基础能力 | 阿里倚天710支持特性：DDR PMU、PCIe PMU驱动支持、CMN-700、RAS | 同左 | NA |  |
|  | ARM架构支持ARM SPE perf memory profiling/c2c特性 |  |  |  |
|  | ARM 64架构支持Memory hotplug |  |  |  |
|  | ARM64架构支持PV-Panic、PV-Unhalt、PV-Preempt特性 |  |  |  |
|  | ARM64架构支持内核热补丁 |  |  |  |
| ARM特性 | ARMv8.5 特性透出   | 同左 | NA |  |
|  | SVE2 能力透出 |  |  |  |
|  | GICv3 中断优先级支持   |  |  |  |
|  | ARM 原子操作优化   |  |  |  |
|  | Hugetlb 迁移支持    |  |  |  |
|  | ARM MTE 支持 |  |  |  |
| ARM漏洞 | 修复多个ARM安全漏洞： | 同左 | NA |  |
|  | 修复重要安全漏洞CVE-2022-1016、CVE-2022-27666 |  |  |  |
|  | 修复CVE-2022-0435、CVE-2022-0847漏洞 |  |  |  |
| 网络 | 比开源增加 | 同ALinux3 | kernel自带 |
|  |  1. tcp网络栈 4.18 |  |  |
|  |  2. 新增 tcp 拥塞算法： BBR， NV |  |  |
|  |  3. nftables替代iptables ， IPVLAN virtual network drivers |  |  |
|  |  4. eXpress Data Path (XDP) feature |  |  |
|  |  5. 默认networkmanager 替代 network-scripts |  |  |
| 存储 | 1. XFS 文件系统支持 shared copy-on-write data extent functionality | 同ALinux3 | kernel自带 |  |
|  | 2. XFS 最大支持1024T |  |  |  |
|  | 3. ext4 文件系统支持 metadata checksum |  |  |  |
|  | 4. NVMe over RDMA is supported |  |  |  |
| 加解密 | 1. 默认使用 Transport Layer Security (TLS) 1.3 在大部分 back-end crypto libraries. | 同ALinux3 | kernel自带 |  |
|  | 2. nss性能改进（用 SQL file format for the trust database by default） |  |  |  |
| 安全 | 1. 默认不再使用 DSA keys 做验证 | 同ALinux3 | kernel自带 |  |
|  | 2. TLS 1.0 and TLS 1.1 默认不再使用 |  |  |  |
| 应用 | 数据库 | MariaDB 10.3, MySQL 8.0, PostgreSQL 10, PostgreSQL 9.6, Redis 5 | 同ALinux3 | NA |
| web server | nginx-1.16 到1.20（acops tuning options） | 同ALinux3 | nginx-1.10 |  |

