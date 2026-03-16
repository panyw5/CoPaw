# CoPaw Console 移动端适配实施计划

## 一、现状分析

### 技术栈
- **前端框架**: React 18 + TypeScript
- **UI 库**: Ant Design 5
- **构建工具**: Vite
- **样式方案**: Less (CSS Modules)
- **路由**: React Router v6

### 当前布局结构
```
MainLayout
├── Sidebar (275px 固定宽度)
│   ├── Logo + Version Badge
│   ├── Collapse Button
│   └── Menu (4 个分组，14 个页面)
├── Layout
    ├── Header (64px 固定高度)
    │   ├── Page Title
    │   ├── 4 个导航按钮 (Changelog, Docs, FAQ, GitHub)
    │   └── Language Switcher
    └── Content
        └── page-content (padding: 0 24px 24px 24px)
```

### 移动端适配现状
- **几乎为零**: 整个 `console/src` 中只有 2 处 `@media` 查询
- **Sidebar**: 275px 固定宽度会占满手机屏幕
- **Header**: 4 个带文字按钮会严重溢出
- **Workspace**: 左右双栏 (400px + flex) 无法在移动端使用
- **表格页面**: 会横向溢出

## 二、适配方案

### 选定方案
- **技术方案**: 纯 CSS 响应式 (`@media` 断点)
- **导航交互**: 底部 Tab 栏 (类似移动 App)
- **断点**: `@media (max-width: 768px)`

### 设计原则
1. **桌面端零影响**: 所有改动仅在移动端生效
2. **渐进增强**: 优先适配高频页面 (Chat, Channels, Skills, Models)
3. **触摸友好**: 按钮最小 44x44px，间距充足
4. **性能优先**: 避免 JS 检测，纯 CSS 实现

## 三、核心改动

### 3.1 底部 Tab 栏设计

#### Tab 项配置
```typescript
主 Tab (5个):
1. 💬 Chat      → /chat
2. 📡 Channels  → /channels
3. ✨ Skills    → /skills
4. 🤖 Models    → /models
5. ⋯  More      → 打开 Drawer

More Drawer 包含:
- Sessions, Cron Jobs, Heartbeat
- Tools, MCP, Workspace, Agent Config
- Environments, Security, Token Usage
```

#### 视觉规范
- **高度**: 56px (iOS 标准)
- **背景**: 白色 + 顶部 1px 边框
- **激活态**: 品牌色 #615ced
- **图标**: 20px, 来自 lucide-react
- **文字**: 10px, 仅在激活时显示

### 3.2 布局适配策略

#### MainLayout 移动端变化
```less
@media (max-width: 768px) {
  // 1. 隐藏 Sidebar
  .sider {
    display: none !important;
  }

  // 2. Content 占满宽度
  .ant-layout {
    width: 100%;
  }

  // 3. 为 TabBar 预留空间
  .page-content {
    padding: 0 12px 68px 12px; // 底部 56px TabBar + 12px 间距
  }
}
```

#### Header 移动端简化
```less
@media (max-width: 768px) {
  .header {
    height: 48px; // 缩小高度
    padding: 0 12px;
  }

  // 隐藏所有导航按钮
  .header button {
    display: none;
  }

  // 只保留标题和语言切换器
  .headerTitle {
    font-size: 16px;
  }
}
```

### 3.3 Workspace 特殊处理

#### 问题
- 左右双栏 (FileListPanel 400px + FileEditor) 无法在移动端并排显示

#### 解决方案
使用 Ant Design Tabs 组件切换视图：

```tsx
// 移动端
<Tabs activeKey={activeTab} onChange={setActiveTab}>
  <TabPane tab="Files" key="files">
    <FileListPanel />
  </TabPane>
  <TabPane tab="Editor" key="editor">
    <FileEditor />
  </TabPane>
</Tabs>

// 桌面端保持原有双栏布局
```

## 四、实施步骤

### Phase 1: 基础布局适配 (核心)

#### 1.1 创建 MobileTabBar 组件
**文件**: `console/src/layouts/MobileTabBar.tsx`

```typescript
import { useNavigate, useLocation } from 'react-router-dom';
import { Drawer } from 'antd';
import { MessageCircle, Wifi, Sparkles, Box, MoreHorizontal } from 'lucide-react';
import styles from './MobileTabBar.module.less';

const MAIN_TABS = [
  { key: 'chat', path: '/chat', icon: MessageCircle, label: 'Chat' },
  { key: 'channels', path: '/channels', icon: Wifi, label: 'Channels' },
  { key: 'skills', path: '/skills', icon: Sparkles, label: 'Skills' },
  { key: 'models', path: '/models', icon: Box, label: 'Models' },
  { key: 'more', path: null, icon: MoreHorizontal, label: 'More' },
];

export default function MobileTabBar({ selectedKey }: { selectedKey: string }) {
  const navigate = useNavigate();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleTabClick = (tab) => {
    if (tab.key === 'more') {
      setDrawerOpen(true);
    } else {
      navigate(tab.path);
    }
  };

  return (
    <>
      <div className={styles.tabBar}>
        {MAIN_TABS.map(tab => (
          <div
            key={tab.key}
            className={`${styles.tabItem} ${selectedKey === tab.key ? styles.active : ''}`}
            onClick={() => handleTabClick(tab)}
          >
            <tab.icon size={20} />
            <span className={styles.tabLabel}>{tab.label}</span>
          </div>
        ))}
      </div>

      <Drawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        placement="bottom"
        height="auto"
      >
        {/* More menu items */}
      </Drawer>
    </>
  );
}
```

**样式**: `console/src/layouts/MobileTabBar.module.less`

```less
.tabBar {
  display: none; // 桌面端隐藏

  @media (max-width: 768px) {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 56px;
    background: #fff;
    border-top: 1px solid #f0f0f0;
    z-index: 1000;
    padding: 0 env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
  }
}

.tabItem {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  color: #999;
  cursor: pointer;
  transition: color 0.2s;

  &.active {
    color: #615ced;
  }
}

.tabLabel {
  font-size: 10px;
  line-height: 1;
}
```

#### 1.2 修改 MainLayout
**文件**: `console/src/layouts/MainLayout/index.tsx`

```typescript
// 添加导入
import MobileTabBar from '../MobileTabBar';

// 在 return 中添加
return (
  <Layout className={styles.mainLayout}>
    <Sidebar selectedKey={selectedKey} />
    <Layout>
      <Header selectedKey={selectedKey} />
      <Content className="page-container">
        {/* ... existing content ... */}
      </Content>
    </Layout>
    <MobileTabBar selectedKey={selectedKey} /> {/* 新增 */}
  </Layout>
);
```

#### 1.3 修改 Sidebar 样式
**文件**: `console/src/layouts/index.module.less`

```less
.sider {
  // ... existing styles ...

  @media (max-width: 768px) {
    display: none !important;
  }
}
```

#### 1.4 修改 Header 样式
**文件**: `console/src/layouts/index.module.less`

```less
.header {
  // ... existing styles ...

  @media (max-width: 768px) {
    height: 48px;
    padding: 0 12px;

    // 隐藏导航按钮，只保留标题和语言切换器
    button:not([class*="language"]) {
      display: none;
    }
  }
}

.headerTitle {
  // ... existing styles ...

  @media (max-width: 768px) {
    font-size: 16px;
  }
}
```

### Phase 2: 全局样式调整

#### 2.1 修改全局布局样式
**文件**: `console/src/styles/layout.css`

```css
@media (max-width: 768px) {
  .page-content {
    padding: 0 12px 68px 12px !important; /* 底部为 TabBar 留空间 */
  }

  /* 所有 Modal 全屏 */
  .ant-modal {
    max-width: 100vw !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  .ant-modal-content {
    border-radius: 0 !important;
  }

  /* Drawer 全屏 */
  .ant-drawer-content-wrapper {
    width: 100% !important;
  }
}
```

#### 2.2 创建移动端通用样式
**新建文件**: `console/src/styles/mobile.css`

```css
/* 移动端通用响应式规则 */
@media (max-width: 768px) {
  /* 卡片网格改为单列 */
  [class*="grid"],
  [class*="Grid"] {
    grid-template-columns: 1fr !important;
  }

  /* 表格横向滚动 */
  .ant-table-wrapper {
    overflow-x: auto;
  }

  /* 按钮组垂直排列 */
  .ant-space-horizontal {
    flex-direction: column !important;
    align-items: stretch !important;
  }

  /* 触摸友好的按钮尺寸 */
  .ant-btn {
    min-height: 44px;
    padding: 8px 16px;
  }

  /* 表单项全宽 */
  .ant-form-item {
    margin-bottom: 16px;
  }

  .ant-input,
  .ant-select,
  .ant-picker {
    font-size: 16px; /* 防止 iOS 自动缩放 */
  }
}
```

### Phase 3: 页面级适配

#### 3.1 Workspace 页面
**文件**: `console/src/pages/Agent/Workspace/index.tsx`

```typescript
import { Tabs } from 'antd';
import { useState, useEffect } from 'react';

export default function WorkspacePage() {
  const [isMobile, setIsMobile] = useState(false);
  const [activeTab, setActiveTab] = useState('files');

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth <= 768);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <div className={styles.agentsPage}>
      {/* ... header ... */}

      {isMobile ? (
        <Tabs activeKey={activeTab} onChange={setActiveTab} className={styles.mobileTabs}>
          <Tabs.TabPane tab="Files" key="files">
            <FileListPanel {...props} />
          </Tabs.TabPane>
          <Tabs.TabPane tab="Editor" key="editor">
            <FileEditor {...props} />
          </Tabs.TabPane>
        </Tabs>
      ) : (
        <div className={styles.content}>
          <FileListPanel {...props} />
          <FileEditor {...props} />
        </div>
      )}
    </div>
  );
}
```

**样式**: `console/src/pages/Agent/Workspace/index.module.less`

```less
@media (max-width: 768px) {
  .agentsPage {
    padding: 12px;
    height: auto;
  }

  .content {
    flex-direction: column;
  }

  .fileListPanel {
    width: 100%;
    max-height: 50vh;
  }

  .mobileTabs {
    flex: 1;

    :global {
      .ant-tabs-content {
        height: calc(100vh - 200px);
        overflow: auto;
      }
    }
  }
}
```

#### 3.2 Skills 页面
**文件**: `console/src/pages/Agent/Skills/index.module.less`

```less
@media (max-width: 768px) {
  .skillsGrid {
    grid-template-columns: 1fr !important;
    gap: 12px;
  }

  .skillCard {
    padding: 12px;
  }

  .descriptionContent {
    min-height: 50px; // 已存在
  }
}
```

#### 3.3 Models 页面
**文件**: `console/src/pages/Settings/Models/index.module.less`

```less
@media (max-width: 768px) {
  .modelFormRow {
    flex-direction: column; // 已存在
    gap: 16px;
  }

  .modelFormItem {
    min-width: unset; // 已存在
    width: 100%;
  }

  .modelCard {
    margin-bottom: 12px;
  }
}
```

#### 3.4 Channels 页面
**新增**: `console/src/pages/Control/Channels/index.module.less`

```less
@media (max-width: 768px) {
  .channelsTable {
    .ant-table {
      font-size: 14px;
    }

    // 隐藏次要列
    .ant-table-cell:nth-child(n+4) {
      display: none;
    }
  }
}
```

### Phase 4: 细节优化

#### 4.1 Chat 页面优化
**文件**: `console/src/pages/Chat/index.module.less`

```less
@media (max-width: 768px) {
  // Chat 组件已经有响应式，只需微调
  :global {
    [class*="chat-anywhere-input"] {
      font-size: 16px; // 防止 iOS 缩放
    }

    [class*="message-bubble"] {
      max-width: 85%; // 移动端气泡更窄
    }
  }
}
```

#### 4.2 Modal 和 Drawer 全屏
**文件**: `console/src/styles/mobile.css`

```css
@media (max-width: 768px) {
  /* 所有 Modal 全屏 */
  .ant-modal {
    max-width: 100vw !important;
    margin: 0 !important;
    top: 0 !important;
    padding-bottom: 0 !important;
  }

  .ant-modal-content {
    border-radius: 0 !important;
    min-height: 100vh;
  }

  .ant-modal-body {
    max-height: calc(100vh - 110px);
    overflow-y: auto;
  }

  /* Drawer 全屏 */
  .ant-drawer-content-wrapper {
    width: 100% !important;
    height: 100% !important;
  }
}
```

## 五、文件清单

### 新建文件 (3 个)
1. `console/src/layouts/MobileTabBar.tsx`
2. `console/src/layouts/MobileTabBar.module.less`
3. `console/src/styles/mobile.css`

### 修改文件 (10+ 个)
1. `console/src/layouts/MainLayout/index.tsx`
2. `console/src/layouts/index.module.less`
3. `console/src/layouts/Header.tsx` (可选)
4. `console/src/styles/layout.css`
5. `console/src/pages/Agent/Workspace/index.tsx`
6. `console/src/pages/Agent/Workspace/index.module.less`
7. `console/src/pages/Agent/Skills/index.module.less`
8. `console/src/pages/Settings/Models/index.module.less`
9. `console/src/pages/Control/Channels/index.module.less`
10. `console/src/pages/Chat/index.module.less`
11. `console/src/App.tsx` (导入 mobile.css)

## 六、测试清单

### 功能测试
- [ ] 底部 Tab 栏在移动端正确显示
- [ ] Tab 切换导航正常
- [ ] More Drawer 打开/关闭正常
- [ ] Sidebar 在移动端完全隐藏
- [ ] Header 在移动端简化显示
- [ ] Workspace 双栏改 Tab 正常切换

### 视觉测试
- [ ] 所有页面在 375px (iPhone SE) 正常显示
- [ ] 所有页面在 768px (iPad) 正常显示
- [ ] 卡片网格改为单列
- [ ] 表格横向滚动正常
- [ ] Modal/Drawer 全屏显示
- [ ] 按钮触摸区域 >= 44px

### 兼容性测试
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] iPad Safari (横屏/竖屏)
- [ ] 桌面端无影响

## 七、风险评估

### 低风险
- ✅ 纯 CSS 方案，不影响现有逻辑
- ✅ 桌面端零改动
- ✅ 使用 Ant Design 原生组件

### 中风险
- ⚠️ Workspace 页面需要 JS 检测屏幕宽度（可用 CSS 替代）
- ⚠️ 第三方 Chat 组件的响应式依赖其自身实现

### 缓解措施
- 充分测试各种屏幕尺寸
- 提供降级方案（横向滚动）
- 分阶段发布，先适配核心页面

## 八、时间估算

- **Phase 1** (基础布局): 4-6 小时
- **Phase 2** (全局样式): 2-3 小时
- **Phase 3** (页面适配): 6-8 小时
- **Phase 4** (细节优化): 2-3 小时
- **测试和修复**: 4-6 小时

**总计**: 18-26 小时

## 九、后续优化

### 可选增强
1. **PWA 支持**: 添加 manifest.json，支持添加到主屏幕
2. **手势操作**: 左右滑动切换 Tab
3. **暗黑模式**: 移动端暗黑主题
4. **性能优化**: 移动端懒加载图片和组件
5. **离线支持**: Service Worker 缓存

### 长期规划
- 考虑使用 React Native 或 Flutter 开发原生 App
- 或使用 Capacitor 将 WebUI 打包为原生 App
