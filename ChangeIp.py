"""
@Author: Xingyu Li
@Email:
32402413@hzcu.edu.cn
@Created on: 2025/3/11 15:43
"""

import time
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import PublicIPAddress
from azure.core.exceptions import HttpResponseError

# Azure 配置
subscription_id =  "xxxx"
resource_group = "xxxx"
ip_name ="xxxx"
location = "xxxx"

# 最大尝试次数
MAX_ATTEMPTS = 100
# 操作之间的等待时间（秒）
WAIT_TIME = 5


def get_credentials():
    """获取 Azure 凭证"""
    try:
        return DefaultAzureCredential()
    except Exception as e:
        print(f"获取凭证失败: {e}")
        exit(1)


def get_network_client(credentials):
    """创建网络管理客户端"""
    return NetworkManagementClient(credentials, subscription_id)


def get_public_ip(client):
    """获取当前公共 IP 地址"""
    try:
        ip_address = client.public_ip_addresses.get(resource_group, ip_name)
        return ip_address.ip_address
    except HttpResponseError as e:
        print(f"获取 IP 地址时出错: {e}")
        return None


def delete_public_ip(client):
    """删除公共 IP 资源"""
    try:
        print("正在删除公共 IP 资源...")
        poller = client.public_ip_addresses.begin_delete(resource_group, ip_name)
        poller.wait()
        print("公共 IP 资源已删除")
        return True
    except HttpResponseError as e:
        print(f"删除 IP 地址时出错: {e}")
        return False


def create_public_ip(client):
    """创建新的公共 IP 资源"""
    try:
        print("正在创建新的公共 IP 资源...")
        poller = client.public_ip_addresses.begin_create_or_update(
            resource_group,
            ip_name,
            {
                'location': location,
                'sku': {
                    'name': 'Standard'
                },
                'public_ip_allocation_method': 'Static',
                'public_ip_address_version': 'IPv4'
            }
        )
        ip_address = poller.result()
        print(f"新的公共 IP 资源已创建: {ip_address.ip_address}")
        return ip_address.ip_address
    except HttpResponseError as e:
        print(f"创建 IP 地址时出错: {e}")
        return None


def main():
    """主函数"""
    if not subscription_id or not resource_group or not ip_name:
        print("请设置必要的环境变量：AZURE_SUBSCRIPTION_ID, AZURE_RESOURCE_GROUP, AZURE_IP_NAME")
        return

    print(f"Azure 配置: 订阅 ID = {subscription_id}, 资源组 = {resource_group}, IP 名称 = {ip_name}")

    credentials = get_credentials()
    network_client = get_network_client(credentials)

    current_ip = get_public_ip(network_client)
    if current_ip:
        print(f"当前 IP 地址: {current_ip}")

    attempt = 0
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        print(f"\n尝试 #{attempt}")

        # 删除当前 IP
        if not delete_public_ip(network_client):
            print("删除 IP 失败，等待后重试...")
            time.sleep(WAIT_TIME)
            continue

        # 创建新 IP
        time.sleep(WAIT_TIME)  # 等待一段时间确保删除操作完成
        new_ip = create_public_ip(network_client)

        if not new_ip:
            print("创建 IP 失败，等待后重试...")
            time.sleep(WAIT_TIME)
            continue

        # 检查是否是 13 段 IP
        if new_ip.startswith("13."):
            print(f"成功获取到 13 段 IP 地址: {new_ip}")
            break
        else:
            print(f"获取到的 IP {new_ip} 不是 13 段，继续尝试...")
            time.sleep(WAIT_TIME)

    if attempt >= MAX_ATTEMPTS:
        print(f"达到最大尝试次数 {MAX_ATTEMPTS}，未能获取 13 段 IP 地址")


if __name__ == "__main__":
    main()
