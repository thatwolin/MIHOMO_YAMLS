import os
import yaml
import re
from urllib.parse import quote
from datetime import datetime

# ================= 配置常量 =================
SOURCE_BASE = "THEYAMLS"
OUTPUT_BASE = "Overwrite/THENEWOPENCLASH"
REPO_RAW = f"https://raw.githubusercontent.com/{os.getenv('GITHUB_REPOSITORY')}/main"

# 处理 YAML 中的 ! 标签
yaml.add_multi_constructor("!", lambda loader, suffix, node: None, Loader=yaml.SafeLoader)

# ==========================================================
# ==== [General] 插件功能配置模板
# ====
# ==== ⚠️  本区块所有功能性配置项均已注释
# ====
# ==== 原因：这些参数会直接覆盖 OpenClash 插件设置，
# ====       如果你已经在 OpenClash 界面里配置好了，
# ====       贸然启用这里的参数会把你的设置覆盖掉。
# ====
# ==== 使用方法：找到你需要的参数，删除该行最前面的 # 号即可启用。
# ====           不确定的参数保持注释状态，插件会使用你自己的界面设置。
# ==========================================================
GENERAL_SECTION = """[General]

# ==========================================================
# ★★★ 必须启用的配置（下载文件和配置路径，模块核心功能）★★★
# 说明：以下三行是本模块的核心，控制从哪里下载 YAML 配置文件，
#       以及告诉 OpenClash 使用哪个文件作为主配置。
#       这三行已在下方动态生成，此处仅作说明。
# ==========================================================

# ==========================================================
# 以下所有参数均为可选，全部默认注释。
# 如需启用某项，请删除该行开头的 # 号。
# 不启用时，OpenClash 会沿用你在插件界面中设置的值。
# ==========================================================


# ----------------------------------------------------------
# 【核心类型】CORE_TYPE
# 说明：指定使用哪个内核。Meta 是常规内核，Smart 是智能内核（支持机器学习策略）。
#       大多数用户使用 Meta 即可，如果你不知道区别，保持注释状态不动。
# 可选值：Meta / Smart
# ----------------------------------------------------------
# CORE_TYPE = Meta


# ==========================================================
# 【DNS 相关】
# 说明：这一组参数控制 OpenClash 如何处理 DNS 请求。
#       如果你的 YAML 配置文件里已经写了完整的 dns 配置，
#       建议不要启用这里的参数，避免产生冲突。
# ==========================================================

# ENABLE_REDIRECT_DNS
# 说明：DNS 重定向模式。控制系统 DNS 流量如何被 OpenClash 接管。
#       0=禁用（不接管 DNS），1=通过 Dnsmasq 转发，2=通过防火墙规则转发。
#       推荐家用路由器使用 1，旁路由使用 2。
# 可选值：0 / 1 / 2
# ----------------------------------------------------------
# ENABLE_REDIRECT_DNS = 1

# ENABLE_CUSTOM_DNS
# 说明：是否让插件用内置规则覆写你的 DNS 配置。
#       0=插件不干涉（完全使用你 YAML 里的 dns 配置），1=启用插件内置规则覆写。
#       如果你的 YAML 里有精心调试过的 dns 配置，建议保持 0（注释状态）。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_CUSTOM_DNS = 1

# APPEND_DEFAULT_DNS
# 说明：是否自动追加 default-nameserver（用于解析 DoH/DoT 服务器的 IP）。
#       0=不追加，1=自动追加插件内置的 default-nameserver。
# 可选值：0 / 1
# ----------------------------------------------------------
# APPEND_DEFAULT_DNS = 1

# APPEND_WAN_DNS
# 说明：是否把路由器 WAN 口分配到的上游 DNS 追加进来。
#       0=不追加，1=追加。在某些网络环境下追加运营商 DNS 可以提升解析速度。
# 可选值：0 / 1
# ----------------------------------------------------------
# APPEND_WAN_DNS = 0

# STORE_FAKEIP
# 说明：是否启用 Fake-IP 缓存（重启后 Fake-IP 映射不丢失）。
#       0=不缓存，1=启用缓存。启用后重启路由器不会导致正在使用的应用断线。
# 可选值：0 / 1
# ----------------------------------------------------------
# STORE_FAKEIP = 1

# CUSTOM_FAKEIP_FILTER
# 说明：是否启用插件内置的 Fake-IP 过滤列表（让某些域名不走 Fake-IP，直接返回真实 IP）。
#       0=不启用，1=启用。常见的局域网、NTP、游戏域名等会自动加入过滤。
# 可选值：0 / 1
# ----------------------------------------------------------
# CUSTOM_FAKEIP_FILTER = 1

# CUSTOM_FAKEIP_FILTER_MODE
# 说明：Fake-IP 过滤模式。blacklist=黑名单（列表内的域名不走 Fake-IP），
#       whitelist=白名单（只有列表内的域名走 Fake-IP）。
#       需要 CUSTOM_FAKEIP_FILTER = 1 才有效。
# 可选值：blacklist / whitelist
# ----------------------------------------------------------
# CUSTOM_FAKEIP_FILTER_MODE = blacklist

# FAKEIP_RANGE
# 说明：自定义 Fake-IP 使用的 IP 地址段。默认 198.18.0.1/16 通常无需修改。
#       只有在该网段与你内网地址冲突时才需要改。
# 示例：198.18.0.1/16
# ----------------------------------------------------------
# FAKEIP_RANGE = 198.18.0.1/16

# ENABLE_RESPECT_RULES
# 说明：DNS 查询是否遵循代理规则（即先查规则再决定用哪个 DNS 解析）。
#       0=不启用，1=启用。启用后可避免 DNS 泄漏，但可能略微增加首次连接延迟。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_RESPECT_RULES = 1

# CUSTOM_NAME_POLICY
# 说明：是否启用插件内置的 Nameserver-Policy（为特定域名指定专用 DNS 服务器）。
#       0=不启用，1=启用。启用后国内域名会走国内 DNS，国外域名走国外 DNS。
# 可选值：0 / 1
# ----------------------------------------------------------
# CUSTOM_NAME_POLICY = 1

# CUSTOM_HOST
# 说明：是否启用插件内置的自定义 Hosts（类似系统 hosts 文件，可强制指定某域名的 IP）。
#       0=不启用，1=启用。
# 可选值：0 / 1
# ----------------------------------------------------------
# CUSTOM_HOST = 1

# CUSTOM_FALLBACK_FILTER
# 说明：是否启用插件内置的 Fallback-Filter（当主 DNS 返回被污染的 IP 时，切换到备用 DNS）。
#       0=不启用，1=启用。开启后可有效防止 DNS 污染。
# 可选值：0 / 1
# ----------------------------------------------------------
# CUSTOM_FALLBACK_FILTER = 1


# ==========================================================
# 【IPv6 相关】
# 说明：控制 IPv6 功能。如果你的网络环境不需要 IPv6 代理，保持注释即可。
# ==========================================================

# IPV6_ENABLE
# 说明：是否启用 IPv6 支持。0=禁用，1=启用。
#       大多数家用场景建议关闭（保持注释），避免 IPv6 流量绕过代理。
# 可选值：0 / 1
# ----------------------------------------------------------
# IPV6_ENABLE = 0

# IPV6_DNS
# 说明：是否启用 IPv6 的 DNS 解析。0=禁用，1=启用。
#       需要 IPV6_ENABLE = 1 才有实际意义。
# 可选值：0 / 1
# ----------------------------------------------------------
# IPV6_DNS = 0


# ==========================================================
# 【代理模式相关】
# 说明：控制 OpenClash 的运行模式和流量处理方式。
#       如果你已经在插件界面配置好了模式，保持这里全部注释即可。
# ==========================================================

# EN_MODE
# 说明：插件的代理模式。fake-ip-mix 是最常用的推荐模式，
#       兼顾兼容性和性能。redir-host 模式适合对 Fake-IP 有顾虑的用户。
# 可选值：fake-ip / fake-ip-tun / fake-ip-mix / redir-host / redir-host-tun / redir-host-mix
# ----------------------------------------------------------
# EN_MODE = fake-ip-mix

# DISABLE_UDP_QUIC
# 说明：是否禁用 QUIC（UDP 443 端口）。1=禁用 QUIC。
#       禁用后浏览器会回退到 TCP，可以避免部分网站因 QUIC 走直连而泄漏流量。
#       推荐启用（设为 1）。
# 可选值：0（允许 QUIC） / 1（禁用 QUIC）
# ----------------------------------------------------------
# DISABLE_UDP_QUIC = 1

# ROUTER_SELF_PROXY
# 说明：路由器自身的流量是否也走代理。0=不走，1=走代理。
#       如果你希望路由器自己访问外网也经过代理，启用此项。
# 可选值：0 / 1
# ----------------------------------------------------------
# ROUTER_SELF_PROXY = 1

# PROXY_MODE
# 说明：代理规则模式。rule=按规则分流（推荐），global=全部走代理，direct=全部直连。
# 可选值：rule / global / direct
# ----------------------------------------------------------
# PROXY_MODE = rule

# STACK_TYPE
# 说明：TUN 模式下的网络栈类型。system 性能最好，gvisor 兼容性最好。
#       只在使用 TUN 模式（fake-ip-tun / redir-host-tun 等）时才有效。
# 可选值：system / gvisor / mixed
# ----------------------------------------------------------
# STACK_TYPE = system


# ==========================================================
# 【防火墙与访问控制】
# 说明：控制谁可以访问 OpenClash 的代理端口。
# ==========================================================

# INTRANET_ALLOWED
# 说明：是否只允许内网设备访问代理。0=允许所有来源，1=仅允许内网。
#       家用路由器场景建议设为 1，安全性更高。
# 可选值：0 / 1
# ----------------------------------------------------------
# INTRANET_ALLOWED = 1

# BYPASS_GATEWAY_COMPATIBLE
# 说明：旁路由（旁路网关）兼容模式。0=关闭，1=开启。
#       只有在旁路由部署场景下才需要开启，主路由保持关闭。
# 可选值：0 / 1
# ----------------------------------------------------------
# BYPASS_GATEWAY_COMPATIBLE = 0


# ==========================================================
# 【分流与国内 IP 绕过】
# 说明：控制国内 IP / 域名是否直连绕过代理，以及流量嗅探功能。
# ==========================================================

# CHINA_IP_ROUTE
# 说明：大陆 IPv4 地址绕行模式。0=禁用，1=大陆 IP 直连绕过代理，2=回国模式（强制走代理）。
#       推荐普通用户设为 1，让国内流量直连，速度更快。
# 可选值：0 / 1 / 2
# ----------------------------------------------------------
# CHINA_IP_ROUTE = 1

# CHINA_IP6_ROUTE
# 说明：大陆 IPv6 地址绕行模式，同上。一般保持 0 即可。
# 可选值：0 / 1 / 2
# ----------------------------------------------------------
# CHINA_IP6_ROUTE = 0

# CHNR_AUTO_UPDATE
# 说明：是否自动更新大陆 IP 列表。0=禁用，1=启用。推荐启用保持列表最新。
# 可选值：0 / 1
# ----------------------------------------------------------
# CHNR_AUTO_UPDATE = 1

# CHNR_UPDATE_WEEK_TIME
# 说明：大陆 IP 列表更新的星期。0=周日，1=周一 ... 6=周六，*=每天。
#       配合 CHNR_UPDATE_DAY_TIME 使用。
# 可选值：0-6 / *
# ----------------------------------------------------------
# CHNR_UPDATE_WEEK_TIME = *

# CHNR_UPDATE_DAY_TIME
# 说明：大陆 IP 列表更新的小时（24小时制）。如 6 代表每天凌晨 6 点更新。
# 可选值：0-23
# ----------------------------------------------------------
# CHNR_UPDATE_DAY_TIME = 6

# ENABLE_META_SNIFFER
# 说明：是否启用域名嗅探（从流量中识别出真实域名，提高分流准确性）。
#       0=不启用，1=启用。强烈推荐启用，否则纯 IP 连接无法正确分流。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_META_SNIFFER = 1

# ENABLE_META_SNIFFER_CUSTOM
# 说明：是否启用插件内置的自定义嗅探规则（更细致的嗅探配置）。
#       需要 ENABLE_META_SNIFFER = 1 才有效。0=不启用，1=启用。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_META_SNIFFER_CUSTOM = 1

# ENABLE_META_SNIFFER_PURE_IP
# 说明：是否对纯 IP 连接（没有域名的流量）也强制进行嗅探。
#       0=不启用，1=启用。启用后可以识别出更多流量的真实目标。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_META_SNIFFER_PURE_IP = 1

# ENABLE_TCP_CONCURRENT
# 说明：是否启用 TCP 并发（同时向多个 DNS 服务器发出查询，取最快的结果）。
#       0=不启用，1=启用。开启后 DNS 解析速度更快，推荐启用。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_TCP_CONCURRENT = 1

# FIND_PROCESS_MODE
# 说明：进程查找模式（用于识别是哪个应用发出的流量）。
#       off=关闭（性能最好），strict=严格模式，always=始终查找。
#       路由器上建议设为 off，OpenWrt 性能有限。
# 可选值：0（不覆写） / off / strict / always
# ----------------------------------------------------------
# FIND_PROCESS_MODE = off

# GLOBAL_CLIENT_FINGERPRINT
# 说明：全局 TLS 客户端指纹伪装，让你的流量看起来像真实浏览器。
#       random=随机选择指纹，推荐使用。
# 可选值：random / chrome / firefox / safari / ios / android / edge / 360 / qq
# ----------------------------------------------------------
# GLOBAL_CLIENT_FINGERPRINT = random

# ENABLE_RULE_PROXY
# 说明：是否只代理命中了规则的流量（未命中规则的流量全部直连）。
#       0=禁用（推荐，MATCH 规则兜底），1=启用（更严格的直连策略）。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_RULE_PROXY = 0

# ENABLE_CUSTOM_CLASH_RULES
# 说明：是否启用插件内置的自定义分流规则（插件会在你的规则前追加一些常用规则）。
#       0=禁用，1=启用。如果你的 YAML 已有完整规则，可以保持 0。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_CUSTOM_CLASH_RULES = 1


# ==========================================================
# 【Smart 智能策略相关】
# 说明：Smart 内核专属功能，使用 LightGBM 机器学习模型自动选择最优节点。
#       只有 CORE_TYPE = Smart 时以下配置才有意义。
# ==========================================================

# AUTO_SMART_SWITCH
# 说明：是否启用 Smart 自动切换（根据模型预测自动选节点）。
#       0=不启用，1=启用。使用 Meta 内核时此项无效。
# 可选值：0 / 1
# ----------------------------------------------------------
# AUTO_SMART_SWITCH = 0

# LGBM_AUTO_UPDATE
# 说明：是否自动更新 LightGBM 机器学习模型文件。
#       0=不启用，1=启用。建议启用保持模型最新。
# 可选值：0 / 1
# ----------------------------------------------------------
# LGBM_AUTO_UPDATE = 1

# LGBM_UPDATE_INTERVAL
# 说明：LightGBM 模型更新间隔，单位为小时。默认 72 小时（3天）更新一次。
# 示例：72
# ----------------------------------------------------------
# LGBM_UPDATE_INTERVAL = 72

# LGBM_CUSTOM_URL
# 说明：LightGBM 模型文件的自定义下载地址。保持默认官方地址即可。
# 默认：https://github.com/vernesong/mihomo/releases/download/LightGBM-Model/Model.bin
# ----------------------------------------------------------
# LGBM_CUSTOM_URL = https://github.com/vernesong/mihomo/releases/download/LightGBM-Model/Model.bin


# ==========================================================
# 【GeoIP / GeoSite 数据库相关】
# 说明：控制地理位置数据库（用于 IP 归属地判断）的加载方式和自动更新。
#       数据库过旧会导致分流不准确，建议启用自动更新。
# ==========================================================

# ENABLE_GEOIP_DAT
# 说明：是否启用 GeoIP Dat 格式数据库（.dat 文件，比 MMDB 更适合 Mihomo 内核）。
#       0=不启用，1=启用。使用 Meta/Smart 内核推荐启用。
# 可选值：0 / 1
# ----------------------------------------------------------
# ENABLE_GEOIP_DAT = 1

# GEODATA_LOADER
# 说明：Geo 数据的加载模式。standard=标准模式（占用内存较多但速度快），
#       memconservative=节省内存模式（适合内存小的设备）。
# 可选值：standard / memconservative / 0（不覆写）
# ----------------------------------------------------------
# GEODATA_LOADER = standard

# GEOIP_AUTO_UPDATE
# 说明：GeoIP Dat 数据是否自动更新。0=禁用，1=启用。推荐启用。
# 可选值：0 / 1
# ----------------------------------------------------------
# GEOIP_AUTO_UPDATE = 1

# GEOIP_UPDATE_WEEK_TIME / GEOIP_UPDATE_DAY_TIME
# 说明：GeoIP Dat 数据更新的时间。WEEK_TIME 控制星期（* 代表每天），
#       DAY_TIME 控制小时（5 代表凌晨 5 点）。
# ----------------------------------------------------------
# GEOIP_UPDATE_WEEK_TIME = *
# GEOIP_UPDATE_DAY_TIME = 5

# GEOSITE_AUTO_UPDATE
# 说明：GeoSite 数据（域名分类库）是否自动更新。0=禁用，1=启用。推荐启用。
# 可选值：0 / 1
# ----------------------------------------------------------
# GEOSITE_AUTO_UPDATE = 1

# GEOSITE_UPDATE_WEEK_TIME / GEOSITE_UPDATE_DAY_TIME
# 说明：GeoSite 数据更新时间，同上。
# ----------------------------------------------------------
# GEOSITE_UPDATE_WEEK_TIME = *
# GEOSITE_UPDATE_DAY_TIME = 5


# ==========================================================
# 【其它功能】
# ==========================================================

# SMALL_FLASH_MEMORY
# 说明：小闪存模式。0=禁用，1=启用。
#       如果你的路由器闪存很小（如 8MB 以下），启用此项可减少写入。
# 可选值：0 / 1
# ----------------------------------------------------------
# SMALL_FLASH_MEMORY = 0

# DISABLE_QUIC_GO_GSO
# 说明：禁用 QUIC Go 的 GSO（Generic Segmentation Offload）优化。
#       0=不禁用，1=禁用。在部分路由器内核上 GSO 有兼容性问题，遇到问题时启用此项。
# 可选值：0 / 1
# ----------------------------------------------------------
# DISABLE_QUIC_GO_GSO = 1

# DELAY_START
# 说明：插件延迟启动的秒数。0=不延迟，数字=延迟对应秒数后再启动。
#       在路由器启动时其他服务还没就绪的情况下，适当延迟可以避免启动失败。
# 示例：0 / 10 / 30
# ----------------------------------------------------------
# DELAY_START = 0

# SKIP_PROXY_ADDRESS
# 说明：是否跳过某些特定地址不走代理（通常指局域网地址）。
#       0=禁用，1=启用插件内置的跳过列表。
# 可选值：0 / 1
# ----------------------------------------------------------
# SKIP_PROXY_ADDRESS = 1

# RESTART
# 说明：覆写模块更新后是否自动重启插件。
#       true=更新后自动重启（使新配置立即生效），false=不自动重启。
#       如果你希望模块更新后立即生效，设为 true。
# 可选值：true / false
# ----------------------------------------------------------
# RESTART = false"""

# ==========================================================
# ==== [General] 下载与订阅部分（动态生成，这3行是模块必须启用的核心）====
# ==========================================================
def build_download_section(raw_url: str, file: str, provider_keys: list) -> str:
    """
    生成下载文件、配置文件路径、订阅信息三行。
    这三行是模块唯一默认启用的 [General] 配置，其余全部注释。
    """
    lines = [
        "",
        "# ==========================================================",
        "# ★★★ 以下三行是本模块核心，默认启用，请勿注释 ★★★",
        "# ==========================================================",
        "#",
        "# DOWNLOAD_FILE：告诉 OpenClash 从哪个 URL 下载你的 YAML 配置文件，",
        "#   下载到路由器的哪个路径，以及多久自动更新一次（cron 表达式）。",
        "#   force=false 表示文件已存在时不强制重新下载。",
        "#   cron=0 6 * * * 表示每天早上 6 点自动更新一次。",
        f"DOWNLOAD_FILE = url={raw_url}, path=/etc/openclash/config/{file}, cron=0 6 * * *, force=false",
        "#",
        "# CONFIG_FILE：告诉 OpenClash 把上面下载的文件作为主配置文件启动。",
        f"CONFIG_FILE = /etc/openclash/config/{file}",
        "#",
        "# SUB_INFO_URL：用于在 OpenClash 界面显示订阅剩余流量信息的 URL。",
        "#   $EN_KEY1 是你在「开发者选项」里填写的第 1 个订阅链接环境变量。",
        "SUB_INFO_URL = $EN_KEY1",
    ]
    return "\n".join(lines)

# ==========================================================
# ==== [YAML] 块 - 新格式核心：proxy-providers url 覆写 ====
# ==========================================================

# 操作符完整参考说明（全部注释，仅作参考）
YAML_OPERATORS_REFERENCE = """# ==========================================================
# ==== YAML 块覆写操作符速查（仅注释参考，如需使用请取消注释）====
# ==========================================================
#
# 操作符说明：
#   key        → 默认合并（Hash 递归合并，其他直接覆盖）
#   key!       → 强制覆盖整个值
#   key+       → 数组后置追加
#   +key       → 数组前置插入
#   key-       → 数组差集删除 / 非数组则删除该键
#   key*       → 批量条件更新（需配合 where/set）
#   <key>后缀  → 同上，适用于键名含特殊字符时
#   +<key>     → 数组前置插入，适用于键名含特殊字符时
#
# 示例（如需启用某条，请删除行首的 #）：
#
# # 向 rules 末尾追加规则
# rules+:
#   - DOMAIN-SUFFIX,example.com,REJECT
#
# # 向 rules 开头插入高优先级规则
# +rules:
#   - DOMAIN-SUFFIX,priority.com,DIRECT
#
# # 强制覆盖整个 dns 配置
# dns!:
#   enable: true
#   nameserver:
#     - '114.114.114.114'
#
# # 批量条件更新：为所有 url-test 组追加节点
# proxy-groups*:
#   where:
#     type: url-test
#   set:
#     proxies+:
#       - 'new-proxy'
#
# # 批量条件更新：按名称正则匹配
# proxy-groups*:
#   where:
#     name: '/^HK/'
#   set:
#     +proxies:
#       - 'hk-new-proxy'
#
# =========================================================="""


def build_yaml_section(provider_keys: list) -> str:
    """
    生成 [YAML] 块：
    - 只生成 proxy-providers 的 url 覆写（批量条件更新），其余全部注释
    - 每个 provider 单独生成一条 proxy-providers* 批量更新，按 name 匹配替换 url 为环境变量
    """
    lines = []
    lines.append("")
    lines.append("# ==========================================================")
    lines.append("# ==== YAML 块覆写标记（新格式核心功能）====")
    lines.append("# ==========================================================")
    lines.append("[YAML]")
    lines.append("")
    lines.append(YAML_OPERATORS_REFERENCE)
    lines.append("")
    lines.append("# ==========================================================")
    lines.append("# ==== proxy-providers URL 覆写（核心功能，已启用）====")
    lines.append("# ==== 用户需在 OpenClash -> 覆写设置 -> 开发者选项中")
    lines.append("# ==== 设置对应的环境变量 EN_KEY1, EN_KEY2 ... ====")
    lines.append("# ==========================================================")

    for idx, name in enumerate(provider_keys, 1):
        lines.append("")
        lines.append(f"# Provider: {name} → 环境变量 $EN_KEY{idx}")
        lines.append(f"proxy-providers*:")
        lines.append(f"  where:")
        lines.append(f"    name: '{name}'")
        lines.append(f"  set:")
        lines.append(f"    url: '$EN_KEY{idx}'")

    return "\n".join(lines)


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def gen_openclash_new():
    print("🚀 开始生成新版 OpenClash 覆写配置（YAML 格式）...")
    os.makedirs(OUTPUT_BASE, exist_ok=True)

    total_count = 0
    categories = {}  # 用于存储分类和文件信息

    for root, dirs, files in os.walk(SOURCE_BASE):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if not file.endswith(('.yaml', '.yml')):
                continue

            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                providers = data.get('proxy-providers', {}) if isinstance(data, dict) else {}
                if not providers:
                    continue

                # 计算路径
                rel_dir = os.path.relpath(root, SOURCE_BASE)
                out_dir = os.path.join(OUTPUT_BASE, rel_dir)
                os.makedirs(out_dir, exist_ok=True)

                # 准备变量
                raw_url = f"{REPO_RAW}/{quote(f'{SOURCE_BASE}/{rel_dir}/{file}'.replace(os.sep, '/'))}"

                # 新格式输出文件名同样用 .yaml 扩展名（新版 OpenClash 覆写模块格式）
                out_name = os.path.splitext(file)[0] + ".yaml"
                out_file = os.path.join(out_dir, out_name)
                provider_keys = list(providers.keys())

                # ==== 生成文件内容 ====
                content_lines = []

                # 文件头注释
                content_lines.append(f"# OpenClash New Overwrite Config for {file}")
                content_lines.append(f"# Generated at: {get_current_date()}")
                content_lines.append(f"# Original Source: {raw_url}")
                content_lines.append(f"# Format: New OpenClash Overwrite Module (YAML)")
                content_lines.append("")

                # 1. [General] 功能性插件配置
                content_lines.append(GENERAL_SECTION)

                # 2. 下载/订阅配置（动态，追加到 General 区域末尾）
                content_lines.append(build_download_section(raw_url, file, provider_keys))

                # 3. [YAML] 块：proxy-providers url 覆写
                content_lines.append(build_yaml_section(provider_keys))

                # 写入文件
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write("\n".join(content_lines))

                # 收集信息用于生成 README
                if rel_dir not in categories:
                    categories[rel_dir] = []
                categories[rel_dir].append({
                    'name': out_name,
                    'source': file,
                    'providers': provider_keys,
                    'raw_url': f"{REPO_RAW}/{quote(f'{OUTPUT_BASE}/{rel_dir}/{out_name}'.replace(os.sep, '/'))}"
                })

                total_count += 1
                print(f"  ✅ 生成: {out_file}  ({len(provider_keys)} 个 provider)")

            except Exception as e:
                print(f"  ⚠️ 处理出错 {file}: {e}")

    # ==== 生成分类 README ====
    for cat, items in categories.items():
        cat_path = os.path.join(OUTPUT_BASE, cat)
        readme_lines = [
            f"# 📁 分类: {cat}",
            "",
            "此目录下为新版 OpenClash 覆写配置文件（YAML 格式），支持新版 YAML 块覆写语法。",
            "",
            "| 配置文件 (.yaml) | 需要填写的订阅源 (Provider) | 操作 |",
            "| :--- | :--- | :--- |"
        ]

        for item in sorted(items, key=lambda x: x['name']):
            prov_str = "<br>".join([f"`$EN_KEY{i+1}`: {p}" for i, p in enumerate(item['providers'])])
            link = item['raw_url']
            readme_lines.append(f"| **{item['name']}** | {prov_str} | [查看源码]({link}) |")

        readme_lines.extend(["", "---", f"[🔙 返回总览](../README.md)"])

        with open(os.path.join(cat_path, "README.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(readme_lines))

    # ==== 生成主 README ====
    main_readme = [
        "# 📦 OpenClash 新版覆写配置仓库",
        "",
        "自动生成基于新版 OpenClash 覆写模块格式的配置文件（`.yaml`）。",
        "每个文件的 `[General]` 功能配置**全部注释**（附详细说明），按需取消注释即可；",
        "`[YAML]` 块仅启用 `proxy-providers` 的 URL 覆写，其余操作均已注释供参考。",
        "",
        "## 📋 与旧版 (.conf) 的区别",
        "",
        "| 对比项 | 旧版 (.conf) | 新版 (.yaml) |",
        "| :--- | :--- | :--- |",
        "| 覆写方式 | `ruby_map_edit` 脚本调用 | `[YAML]` 块操作符（原生） |",
        "| YAML 操作 | 仅支持 key-path 替换 | 支持合并/强制覆盖/追加/删除/条件批量更新 |",
        "| 文件扩展名 | `.conf` | `.yaml` |",
        "| 输出目录 | `Overwrite/THEOPENCLASH/` | `Overwrite/THENEWOPENCLASH/` |",
        "",
        "## 📂 目录总览",
        "",
        "| 分类目录 | 包含配置数 | 说明 |",
        "| :--- | :--- | :--- |"
    ]

    for cat in sorted(categories.keys()):
        count = len(categories[cat])
        main_readme.append(f"| 📁 **[{cat}](./{cat}/README.md)** | {count} 个 | [点击浏览详细列表](./{cat}/README.md) |")

    main_readme.extend([
        "",
        "## 🚀 使用方法",
        "1. 进入上方分类目录找到需要的 `.yaml` 文件。",
        "2. 复制文件 Raw URL。",
        "3. 在 OpenClash -> 覆写设置 -> 覆写模块中添加该 URL。",
        "4. **重要**：在覆写设置 -> 开发者选项中设置对应的环境变量（`EN_KEY1`, `EN_KEY2` 等为你的订阅链接）。",
        "",
        "[🏠 返回项目主页](../../README.md)"
    ])

    with open(os.path.join(OUTPUT_BASE, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(main_readme))

    print(f"✅ 新版覆写配置生成完毕！共处理 {total_count} 个文件。")


if __name__ == "__main__":
    gen_openclash_new()
