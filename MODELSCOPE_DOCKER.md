# CoPaw 魔搭 Docker 部署指南

## 📦 使用 Docker 部署到魔搭创空间

### 方案选择

项目提供了两个 Dockerfile:

1. **Dockerfile** (根目录) - 简化版,适合魔搭快速部署
2. **deploy/Dockerfile** - 完整版,包含浏览器自动化等完整功能

**推荐**: 使用根目录的 `Dockerfile` (已优化)

## 🚀 魔搭创空间配置步骤

### 1. 创建创空间

访问 https://modelscope.cn/ 并登录

### 2. 选择 SDK 类型

选择: **Docker (beta)**

### 3. 配置代码来源

- **仓库地址**: `https://github.com/panyw5/CoPaw.git`
- **分支**: `modelscope-deploy`
- **Dockerfile 路径**: `Dockerfile` (根目录)

### 4. 端口配置

- **容器端口**: `7860`
- **协议**: HTTP

### 5. 环境变量 (可选)

在创空间设置中添加:

```bash
# LLM API Key (必需)
DASHSCOPE_API_KEY=your_dashscope_api_key

# 或使用其他提供商
OPENAI_API_KEY=your_openai_api_key

# 端口配置 (默认 7860)
COPAW_PORT=7860

# 工作目录 (默认 /app/working)
COPAW_WORKING_DIR=/app/working
COPAW_SECRET_DIR=/app/working.secret
```

### 6. 资源配置

建议配置:
- **CPU**: 2 核或以上
- **内存**: 4GB 或以上
- **存储**: 10GB 或以上

### 7. 启动

点击 **创建并启动**,等待构建完成 (首次约 10-15 分钟)

## 📝 部署后配置

### 访问 Console

部署成功后,打开创空间提供的 URL,你会看到 CoPaw Console 界面。

### 配置 API Key

1. 进入 **Settings → Models**
2. 选择 LLM 提供商 (DashScope、OpenAI 等)
3. 输入 API Key
4. 启用模型

### 配置渠道 (可选)

在 **Settings → Channels** 配置钉钉、飞书等渠道。

## 🔧 Dockerfile 说明

### 根目录 Dockerfile (推荐)

**特点**:
- 基于 Python 3.11 slim 镜像
- 多阶段构建,自动构建前端
- 精简依赖,构建速度快
- 适合魔搭环境

**构建过程**:
1. Stage 1: 使用 Node.js 构建前端
2. Stage 2: 安装 Python 依赖和 CoPaw
3. 自动初始化配置
4. 暴露 7860 端口

### deploy/Dockerfile (完整版)

**特点**:
- 包含 Chromium 浏览器
- 支持浏览器自动化
- 包含更多系统依赖
- 镜像较大,构建时间长

**使用场景**:
- 需要浏览器自动化功能
- 需要完整的桌面环境
- 本地 Docker 部署

## 🐛 常见问题

### 1. 构建超时

**原因**: 魔搭构建时间限制

**解决**:
- 使用根目录的简化版 Dockerfile
- 确保网络连接稳定
- 可以尝试多次构建

### 2. 前端资源 404

**原因**: 前端未正确构建

**解决**:
- 确保使用 `modelscope-deploy` 分支
- 该分支已包含预构建的前端资源
- 检查 Dockerfile 的 COPY 指令

### 3. 端口无法访问

**原因**: 端口配置不正确

**解决**:
- 确保 Dockerfile EXPOSE 7860
- 确保 CMD 启动命令使用 `--port 7860`
- 检查魔搭创空间的端口配置

### 4. 内存不足

**原因**: 构建或运行时内存不足

**解决**:
- 增加创空间的内存配置
- 使用简化版 Dockerfile
- 减少并发请求

### 5. 依赖安装失败

**原因**: 某些依赖在魔搭环境不可用

**解决**:
- 检查 requirements.txt
- 移除不必要的依赖
- 使用国内镜像源

## 🔄 更新部署

当你更新代码后:

1. **提交到 main 分支**:
   ```bash
   git checkout main
   git add .
   git commit -m "your changes"
   git push fork main
   ```

2. **更新 modelscope-deploy 分支**:
   ```bash
   git checkout modelscope-deploy
   git merge main
   git push fork modelscope-deploy
   ```

3. **魔搭自动重新构建**:
   - 魔搭会检测到分支更新
   - 自动触发重新构建
   - 等待构建完成

## 💡 优化建议

### 1. 使用构建缓存

在 Dockerfile 中合理安排 COPY 顺序:
- 先复制 requirements.txt 并安装依赖
- 再复制源代码
- 这样依赖层可以被缓存

### 2. 精简镜像

- 使用 slim 基础镜像
- 清理 apt 缓存
- 使用 .dockerignore 排除不必要文件

### 3. 多阶段构建

- 前端构建在独立阶段
- 只复制构建产物到最终镜像
- 减小最终镜像大小

## 📚 参考资源

- [CoPaw 官方文档](https://copaw.agentscope.io/)
- [魔搭 Docker 部署文档](https://modelscope.cn/docs/studios/docker)
- [Dockerfile 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

## 🆘 获取帮助

如遇问题:
1. 查看创空间日志
2. 查看 [GitHub Issues](https://github.com/agentscope-ai/CoPaw/issues)
3. 加入 [Discord 社区](https://discord.gg/eYMpfnkG8h)

---

**提示**: Docker 部署是最推荐的方式,可以完整运行 CoPaw 的所有功能。
