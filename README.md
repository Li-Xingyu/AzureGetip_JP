# AzureGetip_JP

## 参数说明及获取方法

脚本中需要以下几个关键参数：

### 1. subscription_id

这是您的 Azure 订阅 ID，获取方法：
- 登录 [Azure 门户](https://portal.azure.com/)
- 在左侧导航栏中点击"订阅"
- 在订阅列表中找到并复制您要使用的订阅 ID

### 2. resource_group

这是 Azure 中的资源组名称，获取或创建方法：
- 登录 [Azure 门户](https://portal.azure.com/)
- 在左侧导航栏中点击"资源组"
- 可以使用现有的资源组，或点击"创建"按钮创建新的资源组
- 创建资源组时需要指定名称和区域

### 3. ip_name

这是公共 IP 资源的名称，可以自定义设置：
- 在 Azure 门户中，导航到"公共 IP 地址"
- 点击"创建"按钮
- 在创建过程中，您可以指定一个唯一的名称
- 也可以直接在脚本中设置一个新名称，脚本将创建此名称的公共 IP

### 4. location

这是 Azure 区域代码，表示资源的物理位置，例如：
- japaneast（日本东部）
- eastus（美国东部）
- westeurope（西欧）
- 完整的区域列表可在 [Azure 区域页面](https://azure.microsoft.com/zh-cn/explore/global-infrastructure/geographies/) 查看

## 安装 Azure CLI

要使用此脚本，您需要安装 Azure CLI：

1. 访问 [Azure CLI 官方安装介绍](https://docs.microsoft.com/zh-cn/cli/azure/install-azure-cli)
2. 根据您的操作系统选择相应的安装指南
3. 安装完成后，运行以下命令登录您的 Azure 账户：
   ```
   az login
   ```

## 安装依赖

运行脚本前，请安装所需的 Python 依赖包：

```bash
pip install azure-identity azure-mgmt-network
```
