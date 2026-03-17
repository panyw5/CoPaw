import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Drawer, Menu, Space } from "antd";
import { useTranslation } from "react-i18next";
import {
  MessageCircle,
  Wifi,
  Sparkles,
  Box,
  MoreHorizontal,
  UsersRound,
  CalendarClock,
  Activity,
  Wrench,
  Plug,
  Briefcase,
  Settings,
  Globe,
  Shield,
  BarChart3,
} from "lucide-react";
import LanguageSwitcher from "../components/LanguageSwitcher";
import styles from "./MobileTabBar.module.less";

const MAIN_TABS = [
  { key: "chat", path: "/chat", icon: MessageCircle },
  { key: "channels", path: "/channels", icon: Wifi },
  { key: "skills", path: "/skills", icon: Sparkles },
  { key: "models", path: "/models", icon: Box },
  { key: "more", path: null, icon: MoreHorizontal },
];

const MORE_MENU_ITEMS = [
  {
    key: "control-group",
    label: "nav.control",
    children: [
      { key: "sessions", path: "/sessions", icon: UsersRound },
      { key: "cron-jobs", path: "/cron-jobs", icon: CalendarClock },
      { key: "heartbeat", path: "/heartbeat", icon: Activity },
    ],
  },
  {
    key: "agent-group",
    label: "nav.agent",
    children: [
      { key: "workspace", path: "/workspace", icon: Briefcase },
      { key: "tools", path: "/tools", icon: Wrench },
      { key: "mcp", path: "/mcp", icon: Plug },
      { key: "agent-config", path: "/agent-config", icon: Settings },
    ],
  },
  {
    key: "settings-group",
    label: "nav.settings",
    children: [
      { key: "environments", path: "/environments", icon: Globe },
      { key: "security", path: "/security", icon: Shield },
      { key: "token-usage", path: "/token-usage", icon: BarChart3 },
    ],
  },
];

interface MobileTabBarProps {
  selectedKey: string;
}

export default function MobileTabBar({ selectedKey }: MobileTabBarProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleTabClick = (tab: (typeof MAIN_TABS)[0]) => {
    if (tab.key === "more") {
      setDrawerOpen(true);
    } else if (tab.path) {
      navigate(tab.path);
    }
  };

  const handleMoreMenuClick = ({ key }: { key: string }) => {
    const findPath = (items: typeof MORE_MENU_ITEMS): string | null => {
      for (const group of items) {
        const item = group.children?.find((child) => child.key === key);
        if (item?.path) return item.path;
      }
      return null;
    };

    const path = findPath(MORE_MENU_ITEMS);
    if (path) {
      navigate(path);
      setDrawerOpen(false);
    }
  };

  const moreMenuItems = MORE_MENU_ITEMS.map((group) => ({
    key: group.key,
    label: t(group.label),
    type: "group" as const,
    children: group.children.map((item) => ({
      key: item.key,
      label: t(`nav.${item.key.replace(/-([a-z])/g, (_, c) => c.toUpperCase())}`),
      icon: <item.icon size={16} />,
    })),
  }));

  return (
    <>
      <div className={styles.tabBar}>
        {MAIN_TABS.map((tab) => {
          const Icon = tab.icon;
          const isActive = selectedKey === tab.key;
          const label = tab.key === "more" ? t("nav.more") : t(`nav.${tab.key}`);

          return (
            <div
              key={tab.key}
              className={`${styles.tabItem} ${isActive ? styles.active : ""}`}
              onClick={() => handleTabClick(tab)}
            >
              <Icon size={20} />
              <span className={styles.tabLabel}>{label}</span>
            </div>
          );
        })}
      </div>

      <Drawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        placement="bottom"
        height="auto"
        title={t("nav.more")}
        className={styles.moreDrawer}
      >
        <Space direction="vertical" style={{ width: "100%" }} size="middle">
          <Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            onClick={handleMoreMenuClick}
            items={moreMenuItems}
            className={styles.moreMenu}
          />
          <div className={styles.languageSwitcherWrapper}>
            <LanguageSwitcher />
          </div>
        </Space>
      </Drawer>
    </>
  );
}
