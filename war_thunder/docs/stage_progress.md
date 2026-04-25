# 阶段完成记录

## 阶段 1：MVP 最小可运行版本

**当前阶段目标**：
- 先把飞行射击核心玩法跑起来，只做单局游戏，不引入菜单、设置、存档。

**本阶段完成功能**：
- 实现玩家战机移动（上下左右），使用 arcade Sprite
- 实现子弹发射系统，子弹向上飞行并自动销毁
- 实现敌机从屏幕上方随机位置生成并向下移动
- 实现碰撞检测：子弹击中敌机、敌机撞击玩家
- 实现分数系统：每击毁一架敌机 +100 分
- 实现生命值系统：玩家初始 3 点生命，被撞击 -1
- 实现游戏结束判定：生命归零触发结束
- 实现键盘控制：方向键/WASD 移动、Space/Z 射击、R 重开、ESC 返回菜单
- 实现 arcade 主菜单界面，支持四个菜单项

**本阶段页面与 UI 完成情况**：

主菜单页 `MenuWindow`：
- 页面标题：`战争飞机雷霆`，使用 arcade.draw_text 渲染
- 四个菜单项：开始游戏、继续游戏、设置、退出游戏
- `↑/↓` 或 `W/S`：切换选中项
- `Enter` 或 `空格`：执行选中项
- 选中项显示为橙色，未选中为白色

游戏页 `GameView`：
- HUD：显示分数、关卡、生命值(血条)
- 玩家战机：青色三角形战斗机，底部区域移动
- 敌机：红色圆形，从上方生成下落
- 子弹：黄色矩形，向上飞行
- `←/→/↑/↓` 或 `A/D/W/S`：移动战机
- `Space` 或 `Z`：发射子弹
- `R`：游戏结束后重新开始
- `ESC`：返回主菜单
- 底部显示操作按键提示

游戏结束 UI：
- 显示 `游戏结束` 红色大字
- 显示 `按 R 重新开始  ESC 返回菜单`

**本阶段完成设计**：
- 建立基础工程目录结构，避免单文件脚本
- 确定入口层（App）、窗口层（MenuWindow/GameView）、模型层（Player/Bullet/Enemy）的边界
- 使用 arcade.View 实现场景切换
- 使用手动绘制替代 Sprite 简化图形渲染
- `EnemyFactory` 统一控制敌机生成间隔
- `App` 负责窗口管理和视图切换

**本阶段数据流设计**：
- 主菜单进入游戏数据流：`MenuWindow.on_key_press()` -> `App.start_game()` -> 创建新 `GameView` -> `window.show_view(game)`
- 游戏输入数据流：`GameView.on_key_press()` -> 添加到 `keys_pressed` 集合 -> `handle_input()` 处理移动和射击
- 敌机生成数据流：`GameView.on_update()` -> `enemy_factory.update(delta_time)` -> 返回新敌机 -> 添加到 `enemy_list`
- 碰撞检测数据流：距离检测 -> 子弹vs敌机、敌机vs玩家 -> 更新分数/生命
- 玩家扣血反馈：被撞击后 `hit_flash = 0.2` 秒闪红

**本阶段核心业务场景完成进度**：
- 主菜单业务场景：已完成开始游戏、退出游戏入口，继续游戏和设置为占位
- 游戏业务场景：已完成移动、射击、敌机生成、碰撞检测、计分、生命值、游戏结束
- 存档业务场景：本阶段未实现
- UI 组件化业务场景：使用 arcade 原生绘制，暂无 UI 组件抽离

**涉及文件**：
- `war_thunder/main.py`
- `war_thunder/requirements.txt`
- `war_thunder/.gitignore`
- `war_thunder/src/app.py`
- `war_thunder/src/constants.py`
- `war_thunder/src/menu_window.py`
- `war_thunder/src/game_window.py`
- `war_thunder/src/models/__init__.py`
- `war_thunder/src/models/player.py`
- `war_thunder/src/models/bullet.py`
- `war_thunder/src/models/enemy.py`
- `war_thunder/src/models/enemy_factory.py`

**验证情况**：
- 语法检查通过
- 游戏可正常启动运行
- 玩家战机为三角形战斗机形状
- 血条显示在左上角(绿/橙/红色)
- 敌机撞击玩家会扣血并闪红
- 已提交并推送到 GitHub

**下一阶段建议**：
- 工程优化：抽离场景公共接口和基础 UI 组件
- 修复菜单和游戏内按键响应问题
- 增加继续游戏、设置页面
- 增加道具系统（火力强化、护盾、炸弹）
- 增加敌机AI行为（追击、包围等）
