# HF Space Keep Alive

通过 GitHub Actions 定时访问 Hugging Face Space，防止因长时间无活动而休眠。

## 工作原理

GitHub Actions 每 15 分钟自动向你的 HF Space 发送一次 HTTP 请求，模拟用户访问，阻止 Space 进入休眠状态（免费 CPU Space 48 小时无活动会自动暂停）。

支持同时保活多个 Space，支持私有 Space（通过 Token 认证）。

## 配置步骤

### 1. 获取 HF Access Token

前往 [Hugging Face Token 设置](https://huggingface.co/settings/tokens)，创建一个 Access Token（权限选 **Read** 即可）。

### 2. 配置 GitHub Secrets

在仓库 **Settings -> Secrets and variables -> Actions** 中添加以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|---|---|---|
| `HF_TOKEN` | HF Access Token | `hf_xxxxxxxxxx` |
| `SPACE_1` | 第一个 Space 路径 | `username/my-space` |
| `SPACE_2` | 第二个 Space 路径（可选） | `username/my-space-2` |
| `SPACE_3` | 第三个 Space 路径（可选） | `username/my-space-3` |

### 3. 调整 workflow（如有需要）

如果 Space 数量不是 3 个，编辑 `.github/workflows/keepalive.yml`，修改 matrix 列表：

```yaml
strategy:
  matrix:
    space:
      - SPACE_1
      - SPACE_2
      # 增减 Space 在这里修改
```

## 使用方法

### 自动运行

配置完成后无需操作，GitHub Actions 会按 cron 计划每 15 分钟自动执行。

### 手动运行

进入仓库 **Actions** 页面 -> 选择 **Keep HF Spaces Alive** -> 点击 **Run workflow**。

### 查看日志

点击 Actions 中的某次运行记录，展开对应 job 的 **Ping** 步骤，日志格式如下：

```
=== 2026-03-02 12:15:03 UTC ===
Target: SPACE_1
Status Code: 200
Result: OK - Space is alive
```

## 状态码说明

| 状态码 | 含义 |
|---|---|
| `200` | 访问成功，Space 保活正常 |
| `403` | Token 无效或无权限，检查 HF_TOKEN |
| `404` | Space 未找到，检查 Secret 中的路径是否正确 |

## 常见问题

**Q: 支持私有 Space 吗？**

支持。workflow 会在请求头中携带 HF Token 进行认证。

**Q: 如何新增一个 Space？**

1. 在 Secrets 中添加 `SPACE_4`（值为 `用户名/space名`）
2. 在 `keepalive.yml` 的 matrix 列表中添加 `- SPACE_4`

**Q: 15 分钟间隔可以修改吗？**

可以，修改 cron 表达式即可。例如每 30 分钟：`*/30 * * * *`，每 5 分钟：`*/5 * * * *`。

**Q: GitHub Actions 的 cron 准时吗？**

不完全准时，通常会有几分钟延迟，但对保活场景没有影响。

## License

MIT
