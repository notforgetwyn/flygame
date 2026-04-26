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

**当前阶段目标**：
- 实现敌机AI行为（追击、包围）
- 波次系统
- Boss战

**本阶段完成功能**：
- 新增敌机AI类型：NORMAL（直线下落）、HOMING（追踪玩家）、SIDE_ATTACK（横向包抄）、BOSS
- 波次系统：每波敌机数量 = 3 + 波次×2，波次间2秒停顿
- Boss战：每5波出现，10点生命，可发射子弹攻击玩家，击败得500分
- 敌机子弹系统：Boss发射橙色子弹

**本阶段页面与UI完成情况**：

游戏页 `GameScene`：
- HUD新增波次显示（左上角，原关卡位置改为波次）
- Boss头顶显示红色血条
- 不同敌机类型有不同移动行为

**本阶段完成设计**：
- Enemy类增加ai_type属性，根据类型执行不同update逻辑
- EnemyFactory增加波次管理：start_next_wave()、wave_break计时器
- Boss使用独立绘制方法（红色三角形），普通敌机使用圆形纹理
- 新增EnemyBullet类处理Boss子弹

**本阶段数据流设计**：
- EnemyFactory.update()：管理波次和敌机生成，返回None时进入波次停顿
- Enemy.update()：根据ai_type调用update_normal/homing/side/boss
- Enemy.can_shoot()：Boss且bullet_cooldown<=0时可射击
- GameScene.enemy_shoot()：遍历enemies调用can_shoot()和shoot()
- GameScene.check_collisions()：Boss需要多次命中（10点生命），普通敌机1点

**本阶段核心业务场景完成进度**：
- 敌机AI业务场景：已完成（NORMAL、HOMING、SIDE_ATTACK、BOSS四种行为）
- 波次系统业务场景：已完成（数量递增、波次停顿）
- Boss战业务场景：已完成（出现、射击、击杀计分）

**涉及文件**：
- `war_thunder/src/models/enemy.py`
- `war_thunder/src/models/enemy_factory.py`
- `war_thunder/src/constants.py`
- `war_thunder/src/scenes/game_scene.py`

**验证情况**：
- 语法检查通过
- 游戏可正常启动运行
- 不同敌机类型移动行为正确
- Boss出现和射击正常
- 波次递增正常

**下一阶段建议**：
- 阶段5：音效与特效
- 增加爆炸效果
- 增加背景音乐和音效

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
