# 项目交接文档 - Claude 1号 → Claude 2号

## 项目概述
**游戏名称**：战争飞机雷霆（War Thunder Lightning）
**技术栈**：Python + arcade 框架
**项目路径**：D:\flygame\war_thunder

## 快速启动
```bash
cd D:\flygame\war_thunder
powershell -Command "Start-Process -FilePath 'D:\py_3.11\python.exe' -ArgumentList '-m src.app' -WorkingDirectory 'D:\flygame\war_thunder'"
```

注意：`py` 命令指向不存在的 `D:\python3.10`，必须用 `D:\py_3.11\python.exe`

## 已完成阶段

### 阶段1：基础框架
- arcade 框架搭建
- 主菜单、游戏场景
- 玩家战机移动、子弹、敌机生成

### 阶段2：工程优化
- UI组件化（TextBlock、MenuList）
- 设置系统（难度可调）
- 存档系统（自动保存/读档）

### 阶段3：道具系统
- 三种道具：火力强化、护盾、炸弹
- 道具随机掉落（每5秒）+ 击杀掉落（15%概率）
- 道具图标：火力(黄色星)、护盾(蓝色盾)、炸弹(红色雷)

### 阶段4：敌机AI与关卡系统
- 4种敌机AI：NORMAL、HOMING、SIDE_ATTACK、BOSS
- 波次系统：每波数量递增（3 + wave*2），波次间2秒停顿
- Boss：每5波出现，10点生命，可发射子弹，击败得500分

## 核心文件

| 文件 | 说明 |
|------|------|
| `src/app.py` | 应用入口 |
| `src/scenes/game_scene.py` | 游戏主场景 |
| `src/scenes/menu_scene.py` | 主菜单 |
| `src/models/enemy.py` | 敌机类（含EnemyBullet） |
| `src/models/enemy_factory.py` | 敌机工厂（波次管理） |
| `src/models/powerup.py` | 道具类 |
| `src/models/powerup_factory.py` | 道具工厂 |
| `src/constants.py` | 常量定义 |

## 关键常量

```python
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
ENEMY_SPAWN_INTERVAL = 1.5
PLAYER_MAX_HEALTH = 3
SCORE_PER_ENEMY = 100
BOSS_HEALTH = 10
BOSS_SCORE = 500
```

## 当前问题
无严重问题

## 待开发（下一阶段）
阶段5建议：音效与特效
- 爆炸效果
- 背景音乐和音效
- 击中特效

## 开发规范
- 每个阶段创建独立文档 `docs/阶段X.md`
- 阶段完成时提交并推送到 GitHub
- 启动游戏用 PowerShell Start-Process 方式

## Git 操作
```bash
cd /d/flygame
git add <files>
git commit -m "描述"
git push
```
