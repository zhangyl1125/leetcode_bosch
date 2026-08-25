# Pi v0.84.1 卡在 `Working`：官方资料调查

调查日期：2026-08-25

范围：只使用 Pi/OpenAI 官方仓库、官方发行说明、官方文档和 OpenAI 官方状态页。Issue 中的复现事实与报告者推断、未合并补丁严格区分。

## 结论摘要

截图中的启动文案、`openai-codex` provider、`gpt-5.6-luna` model 与 Earendil Works 的官方 Pi coding agent 相符。对应版本为 [`v0.84.1`](https://github.com/earendil-works/pi/releases/tag/v0.84.1)，发布时间为 2026-08-07。

从现有一手证据看，最贴近“发送消息后一直显示 `Working`、没有正文/工具调用/可见错误”的已知问题，是 Pi 官方 issue [#4945](https://github.com/earendil-works/pi/issues/4945)：同样使用 `openai-codex`，交互式 TUI 可在首个流事件之前一直等待；保存下来的 assistant 记录为 `stopReason: "aborted"`、`content: []`，且 usage 全为 0。其次是 Pi 官方 issue [#8331](https://github.com/earendil-works/pi/issues/8331)：provider 流连接仍开着但不再发事件，agent loop 无限等待，spinner 继续转，且 Escape 也无法取消。后者报告使用的正是 Pi `0.84.1`，但案例 provider 是 Anthropic，因此它直接证明的是 provider-neutral 的等待循环症状，不直接证明当前 Codex 请求必然走到了相同故障。

截至调查日，[`v0.84.3`](https://github.com/earendil-works/pi/releases/latest) 是最新发布版；[`v0.84.2`](https://github.com/earendil-works/pi/releases/tag/v0.84.2) 和 `v0.84.3` 的发行说明均未列出对 #4945 或 #8331 的修复，两条 issue 仍处于 open 状态。因此没有官方证据支持“升级即可修复”这一结论。

## 排序后的可能原因

1. **`openai-codex` 在首个流事件之前卡住。** [Pi #4945](https://github.com/earendil-works/pi/issues/4945) 与截图匹配度最高：provider 相同，TUI 长时间只显示 `Working...`，没有 streamed text、tool call 或可见 error；Escape 可终止。该 issue 报告者将其定位为 Codex transport 在首事件前等待，但这部分是报告者分析，不是已经发布的官方根因公告。

2. **已建立的 provider 流静默停止发事件，Pi 继续无限等待。** [Pi #8331](https://github.com/earendil-works/pi/issues/8331) 报告在 `0.84.1` 上 SSE 仍保持连接但没有新事件，spinner 可持续 25–109 分钟，队列消息无法送出，而且 Escape 不生效。若当前卡顿发生在已经输出部分内容之后，或 Escape 完全无效，这个故障形态更匹配。

3. **GPT-5.6 Luna 在超大历史会话中返回“成功但空”的 assistant turn。** [OpenAI Codex #37879](https://github.com/openai/codex/issues/37879) 记录了 GPT-5.6 Luna、ChatGPT subscription/Codex backend 在约 360K–370K input tokens、570+ messages 的大对话中返回 HTTP 200/正常 stop，但 assistant text 为 null、没有 tools、usage 为空或缺失；UI 因而看起来像停住。只有当 `/session` 显示当前会话接近这种规模时，这项才应排在前列；新会话中应显著降级。

4. **账号凭据、provider/model 配置或近期 Codex 认证服务问题。** `v0.84.1` 新增了 [`pi auth check`](https://github.com/earendil-works/pi/releases/tag/v0.84.1)。官方实现需求 [Pi #7152](https://github.com/earendil-works/pi/issues/7152) 说明它可离线检查精确 provider/model 是否存在及凭据是否已配置，不刷新凭据、也不输出凭据值。它不能证明服务端会接受凭据，也不能验证实时网络或生成能力。OpenAI [状态历史](https://status.openai.com/history) 显示 2026-08-20 曾发生 Codex API authentication errors，但已经 resolved；[当前状态页](https://status.openai.com/) 显示整体正常。因此当前大面积 outage 证据较弱，但账户/模型层面的个别问题仍不能由聚合状态页排除。

5. **正常启动加载的 session、context files、extensions 或其他项目资源路径有影响。** 这不是某条 issue 已确认的根因；它是通过 Pi 官方支持的隔离 flags 做出的诊断分支。若最小化、无会话的同模型请求能工作，而普通启动仍卡住，就应把调查范围从 provider transport 转向会话/项目资源路径。

6. **Luna rollout/model 可用性不一致。** [Pi #6601](https://github.com/earendil-works/pi/issues/6601) 曾记录 Luna 通过 `openai-codex` 返回 `Model not found` 404，而 Sol/Terra 可用。该 issue 已关闭、早于 `0.84.1`，而且症状是明确 404，不是静默 `Working`，所以仅在出现对应显式错误时才相关。

其他较低匹配度的一手记录：

- [Pi #8138](https://github.com/earendil-works/pi/issues/8138)：`openai-codex` 偶发返回明确的 “Sorry, something went wrong”，立即重试可成功；它支持 provider 偶发失败的可能性，但不是无错误的持续 `Working`。
- [Pi #7820](https://github.com/earendil-works/pi/issues/7820)：较早的 `openai-codex` 长任务出现 WebSocket 1006/SSE socket close；同样会产生显式 transport error，与截图不完全一致。

## 官方支持的诊断顺序

### 1. 先做不接触服务端的配置检查

依据 `v0.84.1` 的 `auth check` 功能和 [#7152](https://github.com/earendil-works/pi/issues/7152)，可运行：

```bash
pi auth check --provider openai-codex --model gpt-5.6-luna --json --no-refresh
```

该命令只验证本机的配置就绪状态；它不会验证实时服务。Pi 的 [`v0.84.1` provider 文档](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/docs/providers.md) 说明 Codex 登录通过 `/login` 完成，token 存在 `~/.pi/agent/auth.json` 并自动刷新。不要打印、复制或上传该文件。

### 2. 观察 Escape 的行为和最后一条记录

[`v0.84.1` README](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/README.md) 说明 Escape 会 cancel/abort 当前运行，`/session` 会显示 session file、ID、消息数和 token/cost：

- Escape 能立即终止，最后的 assistant record 为 empty content、usage 全 0：高度贴近 [#4945](https://github.com/earendil-works/pi/issues/4945)。
- Escape 不生效、spinner 继续转：更贴近 [#8331](https://github.com/earendil-works/pi/issues/8331)。
- `/session` 显示约 360K–370K input tokens、570+ messages，且 turn 为空：符合 [OpenAI #37879](https://github.com/openai/codex/issues/37879) 的已复现条件。

### 3. 用官方 flags 做一个最小、临时的 live probe

[`v0.84.1` README](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/README.md) 文档化了 provider/model、JSON mode、`--no-session` 及各类 resource-disabling flags；[`json.md`](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/docs/json.md) 说明 JSON mode 会输出 `agent_start`、`turn_start`、`message_start`、delta 和 `message_end` 等事件。下面是由这些官方 flags 组合出的诊断探针，不是官方文档中的原样处方：

```bash
pi --provider openai-codex --model gpt-5.6-luna \
  --mode json --no-session --no-tools --no-extensions \
  --no-skills --no-prompt-templates --no-themes \
  --no-context-files --no-approve "Reply exactly: OK"
```

它会真正请求模型，可能消耗额度，但不保存 session，也不加载项目资源。解释结果：

- 同样在首个 `message_update` 之前卡住：provider/transport 路径的证据增强。
- 最小探针正常、普通启动卡住：session/context/extension 路径的证据增强。
- 出现明确 401/403/404/transport error：按错误本身处理，而不是继续将其归类为无信号的 `Working`。

### 4. 仅在本机检查 debug 日志并先脱敏

Pi 的官方 [`development.md`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/development.md) 说明隐藏命令 `/debug` 会写入 `~/.pi/agent/pi-debug.log`，其中包含渲染后的 TUI 以及最近发送给 LLM 的消息；`v0.84.1` 的 [`config.ts`](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/src/config.ts) 也定义了这一日志路径。日志可能包含用户 prompt、代码或其他敏感上下文，只应在本机检查；分享前必须脱敏。不要分享 `auth.json`、token、Cookie 或 Authorization header。

## 版本与 timeout 证据边界

[Pi PR #4979](https://github.com/earendil-works/pi/pull/4979) 在 2026-05-27 已合并 Codex WebSocket connect/idle timeout。但 maintainer 在 PR 对话中明确说明它“不会修复 #4945”；所以不能把 `v0.84.1` 的症状归因于“完全没有任何 timeout”，也不能声称该合并已经解决首事件前卡住。

[`v0.84.1` settings 文档](https://github.com/earendil-works/pi/blob/v0.84.1/packages/coding-agent/docs/settings.md) 记录了 `transport: "auto"`、`httpIdleTimeoutMs: 300000`、`websocketConnectTimeoutMs: 15000` 等设置。它们适合用于核对当前配置，但现有 issue 中提出的 transport 切换或 timeout 改动属于报告者 workaround/未合并补丁，没有足够官方证据将其作为修复建议。

## 一手来源索引

- Pi 官方仓库：<https://github.com/earendil-works/pi>
- Pi `v0.84.1`：<https://github.com/earendil-works/pi/releases/tag/v0.84.1>
- Pi 最新发行版：<https://github.com/earendil-works/pi/releases/latest>
- 精确 `openai-codex` `Working...` 卡住：<https://github.com/earendil-works/pi/issues/4945>
- `0.84.1` provider stream 静默停止、spinner 无限转：<https://github.com/earendil-works/pi/issues/8331>
- GPT-5.6 Luna 超大会话 empty turn：<https://github.com/openai/codex/issues/37879>
- Codex WebSocket timeout PR 及其适用边界：<https://github.com/earendil-works/pi/pull/4979>
- OpenAI 状态：<https://status.openai.com/>
- OpenAI 状态历史：<https://status.openai.com/history>
