import os
import yaml
from urllib.parse import quote
from datetime import datetime

# ================= 配置常量 =================
SOURCE_BASE = "THEYAMLS"
OUTPUT_BASE = "Overwrite/THENEWOPENCLASH"
REPO_RAW = f"https://raw.githubusercontent.com/{os.getenv('GITHUB_REPOSITORY')}/main"

yaml.add_multi_constructor("!", lambda loader, suffix, node: None, Loader=yaml.SafeLoader)


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def indent_block(text: str, spaces: int = 2) -> str:
    """给多行文本整体加缩进"""
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in text.splitlines())


def comment_block(text: str) -> str:
    """给多行文本每行加 # 注释前缀"""
    result = []
    for line in text.splitlines():
        result.append(("# " + line) if line.strip() else "#")
    return "\n".join(result)


def provider_to_yaml_lines(name: str, config: dict) -> str:
    """
    把单个 provider 的配置序列化为 YAML 文本（不带顶层键名，用于嵌入 proxy-providers* set 块）。
    返回已缩进的多行字符串。
    """
    raw = yaml.dump({name: config}, allow_unicode=True, default_flow_style=False, indent=2)
    return raw.rstrip()


def build_yaml_block(providers: dict) -> str:
    """
    生成完整的 [YAML] 块内容。

    结构：
      [YAML]
      # （操作符参考 + 示例，全部注释）
      # （proxy-providers 各条目，以 proxy-providers* 格式写好，注释状态，取消注释即生效）
    """
    lines = []

    # ── [YAML] 标记 ──────────────────────────────────────────
    lines += [
        "",
        "# ============================================================",
        "# [YAML] 是新版 OpenClash 覆写模块的识别标记，此行不可注释。",
        "# 所有覆写内容均写在此标记之后。",
        "# 注释状态的内容不会生效；取消注释后保存并重新加载模块即可生效。",
        "# ============================================================",
        "[YAML]",
        "",
    ]

    # ── 操作符速查 ────────────────────────────────────────────
    lines += [
        "# ============================================================",
        "# 【操作符速查】",
        "# ------------------------------------------------------------",
        "#  key       默认合并：Hash 递归合并，其他类型直接覆盖",
        "#  key!      强制覆盖：整个值全部替换，不做任何合并",
        "#  key+      数组后置追加：在数组末尾加入新元素",
        "#  +key      数组前置插入：在数组开头插入新元素（规则越靠前越优先）",
        "#  key-      数组差集删除：移除数组中的指定元素；非数组则删除该键",
        "#  key*      批量条件更新：配合 where/set，按条件匹配后批量修改",
        "#  <key>后缀  同上，用于键名含特殊字符（. - /）的情况",
        "#  +<key>    前置插入的 <> 写法",
        "# ============================================================",
        "",
    ]

    # ── 常用示例（全注释）────────────────────────────────────
    lines += [
        "# ============================================================",
        "# 【示例一】在规则列表末尾追加规则（不影响原有规则顺序）",
        "# ------------------------------------------------------------",
        "# +rule-providers:",
        "#   Steam:",
        "#     type: http",
        "#     behavior: domain",
        "#     format: mrs",
        '#     url: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/steam.mrs"',
        "#     interval: 86400",
        "# +rules:",
        "#   - RULE-SET,Steam,Proxy",
        "# ============================================================",
        "",
        "# ============================================================",
        "# 【示例二】在规则列表开头插入高优先级规则（最先匹配）",
        "# ------------------------------------------------------------",
        "# +rules:",
        "#   - DOMAIN-SUFFIX,example.com,DIRECT",
        "#   - IP-CIDR,192.168.0.0/16,DIRECT",
        "# ============================================================",
        "",
        "# ============================================================",
        "# 【示例三】强制替换整个 rules 数组",
        "# ------------------------------------------------------------",
        "# rules!:",
        "#   - DOMAIN-SUFFIX,example.com,DIRECT",
        "#   - MATCH,PROXY",
        "# ============================================================",
        "",
        "# ============================================================",
        "# 【示例四】修改 dns 配置（只改指定字段，其余字段保留）",
        "# ------------------------------------------------------------",
        "# dns:",
        "#   enable: true",
        "#   cache-algorithm: lru",
        "# ============================================================",
        "",
        "# ============================================================",
        "# 【示例五】给所有 url-test 类型策略组的 proxies 末尾追加节点",
        "# ------------------------------------------------------------",
        "# proxy-groups*:",
        "#   where:",
        "#     type: url-test",
        "#   set:",
        "#     proxies+:",
        "#       - '节点名称'",
        "# ============================================================",
        "",
        "# ============================================================",
        "# 【示例六】用正则匹配名称含 HK 的策略组，开头插入节点",
        "# ------------------------------------------------------------",
        "# proxy-groups*:",
        "#   where:",
        "#     name: '/^HK/'",
        "#   set:",
        "#     +proxies:",
        "#       - '香港专线'",
        "# ============================================================",
        "",
    ]

    # ── proxy-providers 内容（核心部分）─────────────────────
    lines += [
        "# ============================================================",
        "# 【proxy-providers 订阅链接替换】",
        "# ------------------------------------------------------------",
        "# 以下每个 proxy-providers* 块对应源文件中的一个 provider，",
        "# 原始配置已完整复制，全部处于注释状态，不会影响任何现有配置。",
        "#",
        "# 使用方法：",
        "#   1. 找到你要替换订阅链接的 provider（看 name: 字段）",
        "#   2. 将该块的 url: 后面的地址换成你自己的订阅链接",
        "#   3. 删除该块所有行最前面的 # 号",
        "#   4. 保存文件，在 OpenClash 中重新加载该覆写模块即可生效",
        "# ============================================================",
        "",
    ]

    for idx, (name, config) in enumerate(providers.items(), 1):
        # 序号标注，方便用户快速定位
        lines.append(f"# ── provider {idx}: {name} " + "─" * max(1, 44 - len(name)))
        lines.append("#")
        lines.append("# proxy-providers*:")
        lines.append("#   where:")
        lines.append(f"#     name: '{name}'")
        lines.append("#   set:")

        # 把原始 provider 配置序列化，以 set: 的子级缩进形式输出，每行加 #
        provider_raw = yaml.dump(config, allow_unicode=True, default_flow_style=False, indent=2)
        for raw_line in provider_raw.rstrip().splitlines():
            # set: 下面的字段需要缩进 4 格（set: 本身缩进 4，字段再缩进 4）
            if raw_line.strip():
                lines.append("#     " + raw_line)
            else:
                lines.append("#")

        lines.append("#")
        lines.append("")

    return "\n".join(lines)


def gen_openclash_new():
    print("🚀 开始生成新版 OpenClash 覆写配置（[YAML] 块格式）...")
    os.makedirs(OUTPUT_BASE, exist_ok=True)

    total_count = 0
    categories = {}

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

                rel_dir = os.path.relpath(root, SOURCE_BASE)
                out_dir = os.path.join(OUTPUT_BASE, rel_dir)
                os.makedirs(out_dir, exist_ok=True)

                raw_url = f"{REPO_RAW}/{quote(f'{SOURCE_BASE}/{rel_dir}/{file}'.replace(os.sep, '/'))}"
                out_name = os.path.splitext(file)[0] + ".yaml"
                out_file = os.path.join(out_dir, out_name)
                provider_keys = list(providers.keys())

                content = "\n".join([
                    f"# OpenClash 覆写模块 - {file}",
                    f"# 生成日期：{get_current_date()}",
                    f"# 源文件：{raw_url}",
                    "# 格式：新版 OpenClash [YAML] 块覆写",
                    "#",
                    "# 本文件仅包含 [YAML] 块覆写内容，不含任何 [General] 插件设置。",
                    "# proxy-providers 内容已原样复制并注释，其余示例均为参考，默认不启用。",
                    build_yaml_block(providers),
                ])

                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(content)

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

    # ==== 分类 README ====
    for cat, items in categories.items():
        cat_path = os.path.join(OUTPUT_BASE, cat)
        readme_lines = [
            f"# 📁 {cat}",
            "",
            "新版 OpenClash 覆写模块（[YAML] 块格式）。",
            "所有内容默认注释，不影响现有配置，取消注释即启用。",
            "",
            "| 文件名 | proxy-providers | Raw 链接 |",
            "| :--- | :--- | :--- |",
        ]
        for item in sorted(items, key=lambda x: x['name']):
            prov_str = "、".join(item['providers'])
            readme_lines.append(
                f"| **{item['name']}** | {prov_str} | [下载/查看]({item['raw_url']}) |"
            )
        readme_lines += ["", "---", "[🔙 返回总览](../README.md)"]
        with open(os.path.join(cat_path, "README.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(readme_lines))

    # ==== 主 README ====
    main_readme = [
        "# 📦 OpenClash 新版覆写模块",
        "",
        "基于新版 OpenClash `[YAML]` 块覆写格式自动生成。",
        "",
        "| | 旧版 `.conf` | 新版 `.yaml` |",
        "| :--- | :--- | :--- |",
        "| url 替换 | `ruby_map_edit` + `$EN_KEY` 环境变量 | `proxy-providers*` 条件更新，直接写链接 |",
        "| 修改能力 | 仅能替换指定路径的值 | 合并 / 强制覆盖 / 追加 / 删除 / 批量条件更新 |",
        "| 默认行为 | 启用后立即覆写 | 全部注释，零影响，按需取消注释 |",
        "",
        "## 📂 目录",
        "",
        "| 分类 | 文件数 |",
        "| :--- | :--- |",
    ]
    for cat in sorted(categories.keys()):
        main_readme.append(f"| 📁 **[{cat}](./{cat}/README.md)** | {len(categories[cat])} 个 |")

    main_readme += [
        "",
        "## 🚀 使用方法",
        "",
        "1. 复制对应 `.yaml` 文件的 Raw URL",
        "2. OpenClash → 覆写设置 → 覆写模块 → 添加 URL",
        "3. 打开文件，找到对应 provider 的 `proxy-providers*` 块",
        "4. 将 `url:` 换成自己的订阅链接，删除该块前面的 `#` 号",
        "5. 重新加载覆写模块生效",
        "",
        "[🏠 返回主页](../../README.md)",
    ]

    with open(os.path.join(OUTPUT_BASE, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(main_readme))

    print(f"✅ 完成！共生成 {total_count} 个覆写文件。")


if __name__ == "__main__":
    gen_openclash_new()
