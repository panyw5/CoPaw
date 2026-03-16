# CoPaw on ModelScope Studio

这是 CoPaw 在魔搭社区创空间的部署版本。

## 关于 CoPaw

CoPaw 是一个个人 AI 助手,可以通过多种渠道(钉钉、飞书、QQ、Discord 等)与你交流,并根据你的配置运行定时任务。

## 使用说明

### 1. 配置 API Key

首次使用需要配置 LLM API Key:

1. 打开 **Settings → Models**
2. 选择一个提供商(如 DashScope)
3. 输入 **API Key**
4. 启用该提供商和模型

### 2. 开始对话

在 Console 界面直接与 CoPaw 对话。

### 3. 配置渠道(可选)

如果想在钉钉、飞书等平台使用:

1. 打开 **Settings → Channels**
2. 选择渠道并配置
3. 详见 [官方文档](https://copaw.agentscope.io/docs/channels)

## 环境变量

可以在 ModelScope Studio 设置中配置:

- `DASHSCOPE_API_KEY`: DashScope API 密钥
- `COPAW_PORT`: 服务端口(默认 7860)

## 文档

- [官方文档](https://copaw.agentscope.io/)
- [GitHub](https://github.com/agentscope-ai/CoPaw)

## 注意事项

- **隐私保护**: 建议将 Studio 设置为**非公开**,防止他人访问
- **数据持久化**: 配置和数据存储在 `/app/working` 目录
- **API Key 安全**: 敏感信息存储在 `/app/working.secret` 目录

## License

Apache License 2.0
