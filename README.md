# daruilab视频提取剪辑skill

把视频、课程或直播整理成可追溯的知识、表达完整的剪辑，以及可复用的代理技能。

本项目将 daruilab 原创的内容提炼与剪辑方法，同 video-to-skill 的时间轴、画面证据和技能生成能力融为一条工作流。按请求执行，不因启用技能而自动下载、剪辑、生成并安装所有产物。

## 能做什么

- 提取带源时间码的逐字稿，保存原始识别稿与核对后的文本。
- 按真实操作顺序还原屏幕提示词、追问、修改与结果。
- 用“是什么、为什么、怎么做、用什么、注意点”提炼金线总结与金句。
- 按完整语义策划多个时长的片段，生成剪辑清单和双语字幕。
- 根据教程画面和口述提取操作步骤，编译、验证、安装独立技能。
- 将新视频补入已有技能，保留来源、确认记录与冲突变体。

## 下载

首版为 **v0.1.0 预发布版**：[版本说明与下载](https://github.com/liudarui6-eng/daruilab-video-extract-edit/releases/tag/v0.1.0)。下载 `daruilab-video-extract-edit-v0.1.0.zip` 并解压，包内含完整技能目录；`SHA256SUMS.txt` 提供下载文件校验值。

融合包版本 v0.1.0 与附带的上游提取器版本 0.2.4 分别编号，不修改上游源码版本。

## 使用方式

将解压后的技能目录（或整个仓库目录）作为技能文件夹放入 Codex 的 `~/.codex/skills/daruilab-video-extract-edit/`，保留 references、scripts、agents 和其余配套文件。已有同名版本时先备份并核对，再替换。重新打开会话后调用：

```text
$daruilab-video-extract-edit
```

也可提供完整请求：

```text
使用 $daruilab-video-extract-edit 分析这个视频，提取完整逐字稿、阶段提示词和金线总结，每项标注源时间码。暂不剪辑。
```

```text
使用 $daruilab-video-extract-edit 从这段视频制作三条约一分钟的精彩剪辑，保留原比例，中文在上、英文在下，并交付字幕和剪辑清单。
```

```text
使用 $daruilab-video-extract-edit 把这份教程整理成可安装技能。精确命令核对画面，保留证据和缺口；安装前展示目标范围。
```

```text
使用 $daruilab-video-extract-edit 将这段新教程合入已有技能，先展示合并预览，保留冲突变体和来源。
```

仅提供视频而没有交付目标时，先确认所需产物。无操作流程的视频不编造步骤来生成技能。

## 工作流与目录

确认交付 → 素材获取 → 转录与时间轴 → 画面核对 → 内容提炼 → 按需剪辑或生成技能 → 验证交付 → 更新。

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 融合后的完整工作流与操作细节 |
| [agents/openai.yaml](agents/openai.yaml) | 显示名称与默认调用提示 |
| [references/](references/) | 素材获取、提炼、分析、剪辑、IR、验证与交付细则 |
| [scripts/validate_edl.py](scripts/validate_edl.py) | 校验正常速度、硬切的单源剪辑清单 |
| [crates/](crates/) | 上游 vts-extract 源码与测试 |
| [SOURCES.md](SOURCES.md) | 原创归属、第三方来源与修改说明 |
| [LICENSE](LICENSE) | video-to-skill 上游 MIT 许可证，非整包统一许可 |
| [UPSTREAM_README.md](UPSTREAM_README.md) | 保留的上游说明，含上游安装与构建资料 |

## 工具与适用边界

先复用本机已有工具与模型；不要求为每项任务安装整套依赖。文字任务优先字幕或音频；媒体处理按需使用 FFmpeg/FFprobe、下载器和本地语音识别工具。完整的提取与技能编译路线使用 vts-extract 0.2.4，工具发现、校验、依赖预览和源码构建方法见主文件。

默认保留原片比例，简体中文上、英文下，使用半透明字幕框。用户可覆盖这些偏好。精确屏幕文字需逐字核对；凭据脱敏，未核对内容明确标注。视频来源命令仅在指定隔离环境内验证。

下载与分析授权不包含发布、付费、绕过访问限制或声音克隆。跨代理安装、同名覆盖及依赖下载按实际授权与工具预览流程执行。

## 来源与版权

- 原 daruilab 部分由 daruilab 原创，版权归 daruilab 所有；目前尚未指定对外使用许可证。
- video-to-skill 来源于 [brenoepics/video-to-skill](https://github.com/brenoepics/video-to-skill)，随附源码声明版本 0.2.4，保留 `Copyright (c) 2026 Breno Epics` 与 MIT 许可证。
- 原方法中对 golden-thread-distill、youtube-video-editor 的参考已注明。
- 原创声明不涵盖第三方代码；上游 MIT 不自动适用于 daruilab 原创部分。完整范围见 [SOURCES.md](SOURCES.md)。

## 当前发布状态

v0.1.0 预发布版。文件完整性、内部引用及剪辑清单校验器的验证结果见 [发布检查记录](RELEASE_CHECKS.md)。尚未宣称完整视频实测、Rust 全部测试通过或正式版本发布。

上游 CI、基准测试和自动发布配置保存在 `.github/upstream-workflows/`，不作为本仓库活动工作流运行；其中含自动下载、写回与发布行为，维护者可核对后按需启用。
