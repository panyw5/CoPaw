# CoPaw 魔搭社区创空间部署指南

本指南介绍如何将 CoPaw 部署到魔搭社区创空间。

## 部署步骤

### 方法一:通过 Git 仓库部署(推荐)

1. **准备代码仓库**

   将你的 CoPaw 代码推送到 Git 仓库(GitHub/Gitee/GitLab):
   ```bash
   git add app.py requirements.txt MODELSCOPE_README.md
   git commit -m "feat: add ModelScope Studio deployment config"
   git push
   ```

2. **创建魔搭创空间**

   - 访问 [魔搭社区](https://modelscope.cn/)
   - 点击 **创空间** → **创建新空间**
   - 选择 **Gradio** 或 **Streamlit** 类型(实际会用 FastAPI)
   - 填写空间信息:
     - 名称: `copaw-custom`
     - 描述: 你的 CoPaw 定制版本
     - **可见性**: 选择 **私有**(重要!)

3. **配置部署**

   在创空间设置中:
   - **代码来源**: 选择 Git 仓库
   - **仓库地址**: 填入你的仓库 URL
   - **分支**: `main` 或你的工作分支
   - **启动文件**: `app.py`
   - **Python 版本**: 3.10 或 3.11

4. **配置环境变量**

   在创空间的 **设置** → **环境变量** 中添加:
   ```
   DASHSCOPE_API_KEY=your_api_key_here
   COPAW_PORT=7860
   ```

5. **启动空间**

   点击 **启动** 按钮,等待部署完成(首次可能需要 5-10 分钟)。

### 方法二:直接上传文件

1. **准备文件**

   确保以下文件在项目根目录:
   - `app.py` - 入口文件 ✅
   - `requirements.txt` - 依赖列表 ✅
   - `MODELSCOPE_README.md` - 说明文档 ✅
   - `src/` - 源代码目录
   - `pyproject.toml` - 项目配置
   - `setup.py` - 安装脚本

2. **创建空间并上传**

   - 创建新的创空间
   - 选择 **文件上传** 方式
   - 上传所有必要文件

3. **配置启动**

   - 启动命令: `python app.py`
   - 端口: `7860`

## 配置说明

### app.py 配置

已创建的 `app.py` 文件包含:
- 自动设置工作目录为 `/app/working`
- 配置端口为 7860(魔搭默认)
- 初始化 CoPaw 应用

### requirements.txt 配置

包含 CoPaw 所有核心依赖:
- FastAPI + Uvicorn (Web 服务)
- AgentScope (AI Agent 框架)
- 各种渠道集成(钉钉、飞书、Discord 等)
- Playwright (浏览器自动化)

### 前端构建

**重要**: 魔搭创空间可能不支持 Node.js 构建。有两种解决方案:

#### 方案 A: 预构建前端(推荐)

在本地构建前端,然后提交:

```bash
cd console
npm ci
npm run build
cd ..

# 将构建产物复制到 src
mkdir -p src/copaw/console
cp -R console/dist/. src/copaw/console/

# 提交到仓库
git add src/copaw/console
git commit -m "feat: add pre-built console assets"
git push
```

#### 方案 B: 使用 Dockerfile

如果魔搭支持 Docker 部署,可以使用项目中的 `deploy/Dockerfile`:

```bash
# 在魔搭创空间设置中
# 构建方式: Docker
# Dockerfile 路径: deploy/Dockerfile
```

## 验证部署

部署成功后:

1. **访问 Console**

   打开创空间提供的 URL,应该看到 CoPaw Console 界面。

2. **配置 API Key**

   - 进入 **Settings → Models**
   - 配置 DashScope 或其他 LLM 提供商
   - 输入 API Key

3. **测试对话**

   在 Console 中发送消息,测试 CoPaw 是否正常响应。

## 常见问题

### 1. 前端资源 404

**原因**: 前端未构建或路径不正确

**解决**: 使用方案 A 预构建前端,确保 `src/copaw/console/` 包含构建产物

### 2. 端口冲突

**原因**: 默认端口 8088 可能不适用于魔搭

**解决**: 在 `app.py` 中已设置为 7860(魔搭默认端口)

### 3. 依赖安装失败

**原因**: 某些依赖可能在魔搭环境不可用

**解决**:
- 移除 `pywebview`(桌面应用相关)
- 移除 `mss`(截图相关)
- 简化 `requirements.txt`,只保留核心依赖

### 4. Playwright 浏览器下载失败

**原因**: 魔搭环境可能无法下载 Chromium

**解决**: 在 `requirements.txt` 中移除 `playwright`,或在环境变量中设置:
```
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
```

## 优化建议

### 1. 精简依赖

对于魔搭部署,可以创建精简版 `requirements.txt`:

```txt
# 核心依赖
agentscope==1.0.16.dev0
agentscope-runtime==1.1.0
fastapi>=0.100.0
uvicorn>=0.40.0
httpx>=0.27.0

# 只保留需要的渠道
# discord-py>=2.3
# dingtalk-stream>=0.24.3

# AI 功能
reme-ai==0.3.0.6b3
transformers>=4.30.0

# 工具
python-dotenv>=1.0.0
aiofiles>=24.1.0
```

### 2. 禁用不需要的功能

在 `app.py` 中添加环境变量:

```python
# 禁用桌面相关功能
os.environ["COPAW_DISABLE_DESKTOP"] = "1"

# 禁用浏览器自动化
os.environ["COPAW_DISABLE_BROWSER"] = "1"
```

### 3. 使用魔搭模型服务

配置使用魔搭的模型 API:

```python
os.environ["MODELSCOPE_API_KEY"] = "your_key"
```

## 下一步

部署成功后,你可以:

1. **配置渠道**: 连接钉钉、飞书等平台
2. **添加技能**: 在 `working/skills/` 目录添加自定义技能
3. **设置定时任务**: 配置 Heartbeat 和 Cron 任务
4. **自定义配置**: 修改 `working/config.json`

## 参考资源

- [CoPaw 官方文档](https://copaw.agentscope.io/)
- [魔搭社区文档](https://modelscope.cn/docs/studios/intro)
- [GitHub 仓库](https://github.com/agentscope-ai/CoPaw)

---

**提示**: 如果遇到问题,可以查看创空间的日志输出,或在 GitHub Issues 提问。
