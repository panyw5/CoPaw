# CoPaw on ModelScope

这是 CoPaw 在魔搭社区的部署版本。

## 🐾 关于 CoPaw

CoPaw 是一个个人 AI 助手,可以通过多种渠道(钉钉、飞书、QQ、Discord 等)与你交流,并根据你的配置运行定时任务。

## 🚀 快速开始

### 1. 配置 API Key

首次使用需要配置 LLM API Key:

1. 打开 Console 界面
2. 进入 **Settings → Models**
3. 选择提供商(如 DashScope)
4. 输入 **API Key**
5. 启用模型

### 2. 开始对话

在 Console 界面直接与 CoPaw 对话。

### 3. 配置渠道 (可选)

如果想在钉钉、飞书等平台使用:

1. 打开 **Settings → Channels**
2. 选择渠道并配置
3. 详见 [官方文档](https://copaw.agentscope.io/docs/channels)

## 🔧 技术栈

- **后端**: FastAPI + AgentScope
- **前端**: React + Ant Design
- **部署**: Docker

## 📝 环境变量

可在魔搭创空间设置中配置:

- `DASHSCOPE_API_KEY`: DashScope API 密钥
- `OPENAI_API_KEY`: OpenAI API 密钥
- `COPAW_PORT`: 服务端口 (默认 7860)

## 📚 文档

- [官方文档](https://copaw.agentscope.io/)
- [GitHub 仓库](https://github.com/agentscope-ai/CoPaw)
- [部署指南](./MODELSCOPE_DOCKER.md)

## ⚠️ 注意事项

- **隐私保护**: 建议将创空间设置为**私有**
- **数据持久化**: 配置和数据存储在 `/app/working` 目录
- **API Key 安全**: 敏感信息存储在 `/app/working.secret` 目录

## 🆘 获取帮助

- [GitHub Issues](https://github.com/agentscope-ai/CoPaw/issues)
- [Discord 社区](https://discord.gg/eYMpfnkG8h)

## 📄 License

Apache License 2.0

---

**Built by**: [AgentScope Team](https://github.com/agentscope-ai)
