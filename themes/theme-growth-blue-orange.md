# 公众号排版组件库 —— 增长蓝橙

> 为「增长研习社」（主笔：李云龙）定制。深蓝作骨架，橙色作锋芒；
> 全文只有蓝、橙两种彩色，不引入第三色。
> 适用：增长方法论、案例复盘、商业观点、数据驱动的深度分析。

**本主题的三条硬规则**（与其它主题不同，装配时别照搬通用流程）：

1. **不做「本文看点」导读卡**。头图 → 引言卡 → 直接进正文。
   不要在正文前插三列目录卡，也不要用任何其它形式的看点罗列。
2. **章节标题不配英文标签**。只有中文标题（可带编号），
   不要 THE PRICE / FIVE VALUES 这类英文小字。
3. **不做文首署名标签**。开头不出现「李云龙主笔」这类橙底标签，
   署名只在文末出现一次（组件 14）。

## 设计变量速查表

| 变量 | 色值 | 用途 |
|------|------|------|
| 主色（深蓝） | `#1B4F8A` | 二级标题、分割线、引用左边框、卡片标题、编号底 |
| 标题深蓝 | `#123A66` | 一级标题文字（比主色更沉，拉开层级） |
| 强调色（橙） | `#FF6B35` | 重点句加粗、关键词下划线、数据标注、一级标题竖条 |
| 正文色 | `#3F3F3F` | 正文主文字（深灰，不用纯黑） |
| 次要文字 | `#8C8C8C` | 图注、来源、辅助说明、文末署名 |
| 浅背景 | `#F7F8FA` | 引用块、卡片、表格隔行 |
| 分割线 | `#E6E8EB` | 细线、卡片描边、表格边框 |
| 背景 | `#FFFFFF` | 文章主背景 |

**只有两种彩色**：`#1B4F8A` / `#123A66` 是同一支蓝的深浅，`#FF6B35` 是唯一的橙。
灰阶（`#3F3F3F` / `#8C8C8C` / `#F7F8FA` / `#E6E8EB`）不算彩色。
任何情况下不要引入红、绿、紫、黄。

**橙色用量**：全文橙色面积控制在 10% 以内。橙是锋芒，铺满就钝了。
一个章节内橙色加粗不超过 2 处，下划线按正文规则每段 1–3 个短语。

> 去掉文首署名标签后，橙色不再有任何实心色块的用法，
> 只剩下：一级标题竖条、关键词下划线、重点加粗文字、数据标注、无序列表圆点、
> 金句引用左条、警示条顶边。全是线条和文字，没有块面。这让橙色更像锋芒而非装饰。

---

## 组件 1 全局容器

```html
<section style="max-width:677px;margin:0 auto;background:#FFFFFF;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#3F3F3F;line-height:1.75;letter-spacing:0.5px;overflow-x:hidden;">
  <!-- 全部内容 -->
</section>
```

## 组件 2 开头引言卡（题记）

头图之后第一个出现的内容块。

```html
<section style="margin:10px 10px 32px;background:#F7F8FA;border-radius:10px;padding:24px 22px 20px;overflow:hidden;">
  <p style="font-size:38px;color:#1B4F8A;font-weight:900;margin:0;line-height:0.6;">
    <span leaf="">“</span>
  </p>
  <p style="font-size:16px;font-weight:700;color:#123A66;margin:12px 0 4px;line-height:1.75;">
    <span leaf="">{题记前半}</span>
    <span style="color:#FF6B35;font-weight:800;"><span leaf="">{关键词1}</span></span>
    <span leaf="">{题记中段}</span>
    <span style="color:#FF6B35;font-weight:800;"><span leaf="">{关键词2}</span></span>
    <span leaf="">{题记后半}</span>
  </p>
</section>
```

题记完整照录，不省字。高亮恰好 2 处，用橙色文字而非橙色底——底色块在深色模式下容易发脏。

**引言卡之后直接进正文，不插导读卡、不插署名标签。**

## 组件 3 章节分割线（蓝色渐变）

```html
<section style="padding:0 10px;">
  <section style="height:1px;background:linear-gradient(to right,transparent,#E6E8EB,#1B4F8A,#E6E8EB,transparent);margin:0;">
    <span leaf=""><br></span>
  </section>
</section>
```

## 组件 4 一级标题（章节标题，18px + 橙色竖条，无英文标签）

`##` 映射到这里。18px，文字 `#123A66`，左侧 3px 橙色竖条。**不加英文小标签。**

```html
<section style="margin-top:48px;margin-bottom:24px;padding:0 10px;">
  <section style="border-left:3px solid #FF6B35;padding-left:12px;">
    <h3 style="font-size:18px;font-weight:800;color:#123A66;margin:0;letter-spacing:0.5px;line-height:1.5;">
      <span leaf="">{章节标题}</span>
    </h3>
  </section>
</section>
```

**带编号的变体**（章节 4 个以上、需要序号感时用）：

```html
<section style="margin-top:48px;margin-bottom:24px;padding:0 10px;">
  <section style="border-left:3px solid #FF6B35;padding-left:12px;">
    <h3 style="font-size:18px;font-weight:800;color:#123A66;margin:0;letter-spacing:0.5px;line-height:1.5;">
      <span style="color:#FF6B35;"><span leaf="">01 </span></span>
      <span leaf="">{章节标题}</span>
    </h3>
  </section>
</section>
```

同一篇文章里只用一种变体，不混用。
没有英文标签之后，标题区只剩单行，上方 `margin-top:48px` 的留白就是层级感的来源，别压缩。

## 组件 4b 二级标题（小节标题，16px 蓝色加粗）

`###` 映射到这里。

```html
<section style="padding:0 10px;">
  <h4 style="font-size:16px;font-weight:700;color:#1B4F8A;margin:28px 0 14px;letter-spacing:0.5px;line-height:1.6;">
    <span leaf="">{小节标题}</span>
  </h4>
</section>
```

## 组件 5 正文段落

```html
<section style="padding:0 10px;">
  <p style="margin-bottom:20px;font-size:15px;line-height:1.8;text-align:justify;color:#3F3F3F;">
    <span leaf="">{正文}</span>
  </p>
</section>
```

连续多段时，外层 `<section style="padding:0 10px;">` 包住整组，不必每段一个。

## 组件 6 正文高亮样式

### 6a. 橙色关键词下划线（最常用，每段 1–3 处）

```html
<span style="border-bottom:2px solid #FF6B35;font-weight:600;"><span leaf="">{关键短语}</span></span>
```

正文关键词标记一律用这一条，权威来源是 `theme-index.md` 的「正文下划线 CSS」列。

### 6b. 橙色重点加粗（锚点层，全文 ≤ 5 处）

```html
<strong style="color:#FF6B35;"><span leaf="">{重点句}</span></strong>
```

不加底色、不用荧光笔效果。橙字本身已经够跳，加底色会在深色模式下糊成一块。

### 6c. 数据标注（橙色加粗，用于数字与指标）

```html
<span style="color:#FF6B35;font-weight:800;"><span leaf="">复购率提升 37%</span></span>
```

数字和单位一起包进去，别只标数字不标单位。
数据标注不计入 6b 的 5 处配额，但同一段里别超过 3 个，否则页面像仪表盘。

### 6d. 蓝色概念标签（核心术语，每篇 2~4 个）

```html
<span style="background:#F7F8FA;color:#1B4F8A;padding:2px 6px;border-radius:3px;font-weight:700;border:1px solid #E6E8EB;"><span leaf="">{核心概念}</span></span>
```

### 6e. 行内代码

```html
<span style="background:#F7F8FA;color:#3F3F3F;padding:1px 5px;border-radius:3px;font-family:Menlo,Consolas,monospace;font-size:14px;border:1px solid #E6E8EB;"><span leaf="">{code}</span></span>
```

## 组件 7 引用块

### 7a. 标准引用（浅底 + 蓝色左条）

```html
<section style="background:#F7F8FA;border-left:3px solid #1B4F8A;border-radius:0 8px 8px 0;padding:16px 20px;margin:0 10px 24px;">
  <p style="font-size:15px;color:#3F3F3F;margin:0;line-height:1.8;text-align:justify;">
    <span leaf="">{引用内容}</span>
  </p>
</section>
```

### 7b. 金句引用（橙色左条，视觉焦点最强）

```html
<section style="background:#F7F8FA;border-left:3px solid #FF6B35;border-radius:0 8px 8px 0;padding:18px 22px;margin:0 10px 24px;">
  <p style="font-size:16px;font-weight:700;color:#123A66;margin:0;line-height:1.8;">
    <span leaf="">{核心金句}</span>
  </p>
</section>
```

一篇文章里 7b 不超过 2 处，多了就不是金句了。

### 7c. 居中金句分隔（章节间过渡）

```html
<section style="padding:0 10px;">
  <p style="font-size:15px;margin:0 0 24px;text-align:center;color:#1B4F8A;font-weight:700;letter-spacing:1px;border-top:1px solid #E6E8EB;border-bottom:1px solid #E6E8EB;padding:14px 10px;">
    <span leaf="">{过渡金句}</span>
  </p>
</section>
```

## 组件 8 提示条

### 8a. 蓝色提示条（重要结论）

```html
<section style="background:#F7F8FA;border:1px solid #E6E8EB;border-top:2px solid #1B4F8A;border-radius:0 0 8px 8px;padding:16px 20px;margin:0 10px 24px;">
  <p style="font-size:13px;color:#1B4F8A;font-weight:800;margin:0 0 8px;letter-spacing:1px;">
    <span leaf="">核心结论</span>
  </p>
  <p style="font-size:15px;color:#3F3F3F;margin:0;line-height:1.8;text-align:justify;">
    <span leaf="">{结论内容}</span>
  </p>
</section>
```

### 8b. 橙色警示条（风险、踩坑）

```html
<section style="background:#F7F8FA;border:1px solid #E6E8EB;border-top:2px solid #FF6B35;border-radius:0 0 8px 8px;padding:16px 20px;margin:0 10px 24px;">
  <p style="font-size:13px;color:#FF6B35;font-weight:800;margin:0 0 8px;letter-spacing:1px;">
    <span leaf="">注意</span>
  </p>
  <p style="font-size:15px;color:#3F3F3F;margin:0;line-height:1.8;text-align:justify;">
    <span leaf="">{风险内容}</span>
  </p>
</section>
```

## 组件 9 列表

### 9a. 有序列表（蓝色方标编号）

```html
<section style="padding:0 10px;margin-bottom:24px;">
  <section style="display:flex;margin-bottom:14px;">
    <span style="display:inline-block;background:#1B4F8A;color:#FFFFFF;font-size:12px;font-weight:800;min-width:20px;height:20px;line-height:20px;text-align:center;border-radius:3px;margin-right:10px;"><span leaf="">1</span></span>
    <span style="flex:1;font-size:15px;color:#3F3F3F;line-height:1.7;"><span leaf="">{条目内容}</span></span>
  </section>
  <section style="display:flex;margin-bottom:14px;">
    <span style="display:inline-block;background:#1B4F8A;color:#FFFFFF;font-size:12px;font-weight:800;min-width:20px;height:20px;line-height:20px;text-align:center;border-radius:3px;margin-right:10px;"><span leaf="">2</span></span>
    <span style="flex:1;font-size:15px;color:#3F3F3F;line-height:1.7;"><span leaf="">{条目内容}</span></span>
  </section>
</section>
```

选项式列表（A / B / C）把编号文字换掉即可，样式不变。

### 9b. 无序要点（橙点前缀）

```html
<section style="padding:0 10px;margin-bottom:24px;">
  <section style="display:flex;margin-bottom:12px;">
    <span style="display:inline-block;width:6px;height:6px;background:#FF6B35;border-radius:50%;margin:9px 10px 0 0;"><span leaf=""><br></span></span>
    <span style="flex:1;font-size:15px;color:#3F3F3F;line-height:1.7;"><span leaf="">{要点内容}</span></span>
  </section>
</section>
```

### 9c. 时间线（增长阶段、案例演进）

```html
<section style="padding:0 10px;margin-bottom:24px;">
  <section style="border-left:2px solid #E6E8EB;padding-left:16px;margin-left:4px;">
    <section style="margin-bottom:18px;">
      <p style="font-size:13px;color:#FF6B35;font-weight:800;margin:0 0 4px;"><span leaf="">{时间/阶段}</span></p>
      <p style="font-size:15px;color:#3F3F3F;margin:0;line-height:1.7;text-align:justify;"><span leaf="">{事件描述}</span></p>
    </section>
  </section>
</section>
```

## 组件 10 数据卡片与表格

### 10a. 数据卡片（两列）

```html
<section style="padding:0 10px 24px;">
  <section style="display:flex;justify-content:space-between;">
    <section style="flex:1;background:#F7F8FA;border:1px solid #E6E8EB;border-radius:8px;padding:18px 14px;margin-right:10px;text-align:center;">
      <p style="font-size:24px;font-weight:800;color:#FF6B35;margin:0 0 6px;line-height:1.2;"><span leaf="">37%</span></p>
      <p style="font-size:13px;color:#8C8C8C;margin:0;"><span leaf="">{指标名}</span></p>
    </section>
    <section style="flex:1;background:#F7F8FA;border:1px solid #E6E8EB;border-radius:8px;padding:18px 14px;text-align:center;">
      <p style="font-size:24px;font-weight:800;color:#FF6B35;margin:0 0 6px;line-height:1.2;"><span leaf="">2.4x</span></p>
      <p style="font-size:13px;color:#8C8C8C;margin:0;"><span leaf="">{指标名}</span></p>
    </section>
  </section>
</section>
```

数据卡片只在原文没有把数字写进句子时用；原文已经写了的，用 6c 行内标注，别重复一遍。

### 10b. 表格（真实数据表）

```html
<section style="padding:0 10px 24px;overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <tbody>
      <tr style="background:#1B4F8A;">
        <th style="padding:10px 12px;color:#FFFFFF;font-weight:700;text-align:left;border:1px solid #E6E8EB;"><span leaf="">{表头1}</span></th>
        <th style="padding:10px 12px;color:#FFFFFF;font-weight:700;text-align:left;border:1px solid #E6E8EB;"><span leaf="">{表头2}</span></th>
      </tr>
      <tr style="background:#FFFFFF;">
        <td style="padding:10px 12px;color:#3F3F3F;border:1px solid #E6E8EB;"><span leaf="">{内容}</span></td>
        <td style="padding:10px 12px;color:#3F3F3F;border:1px solid #E6E8EB;"><span leaf="">{内容}</span></td>
      </tr>
      <tr style="background:#F7F8FA;">
        <td style="padding:10px 12px;color:#3F3F3F;border:1px solid #E6E8EB;"><span leaf="">{内容}</span></td>
        <td style="padding:10px 12px;color:#3F3F3F;border:1px solid #E6E8EB;"><span leaf="">{内容}</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

列宽按内容长度分配，480 宽下不横向溢出，内容一字不删。

## 组件 11 标签胶囊

```html
<section style="padding:0 10px 20px;">
  <span style="display:inline-block;background:#F7F8FA;color:#1B4F8A;font-size:12px;padding:3px 10px;border-radius:12px;margin-right:6px;border:1px solid #E6E8EB;"><span leaf="">{标签}</span></span>
  <span style="display:inline-block;background:#F7F8FA;color:#1B4F8A;font-size:12px;padding:3px 10px;border-radius:12px;margin-right:6px;border:1px solid #E6E8EB;"><span leaf="">{标签}</span></span>
</section>
```

## 组件 12 图片容器

```html
<section style="padding:6px;border:1px solid #E6E8EB;border-radius:10px;margin:10px 10px 24px;">
  <section style="margin:0;border-radius:6px;overflow:hidden;">
    <span leaf=""><img src="{图片地址}" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
  </section>
</section>
```

配图注时，图注用 `#8C8C8C`、13px、居中。

## 组件 13 END 结尾分割线

```html
<section style="padding:0 10px;">
  <section style="text-align:center;margin:0 0 28px;">
    <section style="display:flex;align-items:center;justify-content:center;">
      <span style="height:1px;width:60px;background:linear-gradient(to right,transparent,#1B4F8A);margin-right:12px;"><span leaf=""><br></span></span>
      <span style="font-size:11px;color:#1B4F8A;letter-spacing:3px;font-weight:700;"><span leaf="">END</span></span>
      <span style="height:1px;width:60px;background:linear-gradient(to left,transparent,#1B4F8A);margin-left:12px;"><span leaf=""><br></span></span>
    </section>
  </section>
</section>
```

## 组件 14 尾部签名区

全文唯一的署名位置。

```html
<section style="padding:0 10px;">
  <p style="margin-bottom:20px;font-size:15px;line-height:1.8;text-align:center;color:#8C8C8C;letter-spacing:1px;">
    <span leaf="">—— 李云龙增长研习社</span>
  </p>
</section>
```

只这一句，居中，末尾。不加 CTA、不加作者简介、不加合作方式。

---

## 完整文章模板骨架

装配顺序固定：

```
组件 1  全局容器（包住全部）
├─ 组件 12 头图（封面，全文只出现一次）
├─ 组件 2  开头引言卡（完整题记 + 2 处橙色关键词）
├─ 前言正文（组件 5）          ← 引言卡之后直接进正文
├─ 组件 4  一级标题（纯中文，无英文标签）
│   ├─ 组件 5  正文段落（每段 1–3 处组件 6a 下划线）
│   ├─ 组件 4b 二级标题（有 ### 时）
│   └─ 组件 7 / 8 / 9 / 10（按文章类型配方选）
├─ 组件 3  章节分割线
├─ 组件 4  一级标题
│   └─ ……
├─ 组件 13 END 分割线
└─ 组件 14 尾部签名区
```

**本主题没有目录环节，也没有文首署名**。其它主题的「本文看点」三列卡和
开头作者标签在这里都不适用；通用流程里「目录精选 3 个看点」的检查项，
用本主题时直接跳过。头图之后第一眼看到的就是题记。

## 视觉层级（3 层递进）

| 层 | 手段 | 配额 |
|---|---|---|
| 锚点层 | 组件 6b 橙色加粗 | 全文 ≤ 5 处 |
| 标记层 | 组件 6a 橙色下划线 | 每段 1–3 处，一段都不能漏 |
| 结构层 | 组件 4 / 4b 标题、组件 3 分割线、组件 7 引用块 | 按结构需要 |

数据标注（6c）独立于锚点层配额，但每段 ≤ 3 个。

去掉英文标签之后，章节之间的区分只剩「分割线 + 大留白 + 橙竖条」三样，
所以分割线和 `margin-top:48px` 不能省，省了章节就糊在一起。

## 文章类型 → 组件组合配方

| 文章类型 | 核心组件 | 点缀组件（≤3 种） | 一级标题变体 |
|---------|---------|-----------------|-------------|
| 增长方法论 / 体系拆解 | 5 + 4b + 9a | 8a 蓝色结论条、7a 引用、10a 数据卡 | 带编号 |
| 案例复盘 | 5 + 9c 时间线 + 10a | 7b 金句、8b 警示条 | 带编号 |
| 商业观点 / 评论 | 5 + 7b + 7c | 7a 引用、6d 概念标签 | 4 章以上带编号，否则不带 |
| 数据驱动分析 | 5 + 10a + 10b 表格 | 8a 结论条、6c 数据标注 | 带编号 |
| 工具 / 清单盘点 | 5 + 9a + 11 标签 | 10a 数据卡、8b 警示条 | 带编号 |

## Markdown → 增长蓝橙 映射规则

| Markdown | 组件 | 说明 |
|---------|------|------|
| `#` 一级标题 | 不进正文 | 走公众号标题栏 |
| `> 题记` | 组件 2 引言卡 | 完整照录，2 处橙色关键词高亮 |
| `##` | 组件 4 一级标题 | 18px `#123A66` + 3px 橙竖条，**不配英文标签** |
| `###` | 组件 4b 二级标题 | 16px `#1B4F8A` 加粗 |
| 普通段落 | 组件 5 | 每段 1–3 处 6a 下划线 |
| `**加粗**` | 组件 6b | 橙色加粗，全文 ≤ 5 处 |
| 含数字的指标 | 组件 6c | 数字带单位一起标橙 |
| `> 引用` | 组件 7a | 浅底 + 蓝色左条 |
| 金句 / 核心论点 | 组件 7b | 橙色左条，≤ 2 处 |
| `1. 2. 3.` 有序列表 | 组件 9a | 蓝色方标编号 |
| `- ` 无序列表 | 组件 9b | 橙点前缀 |
| 表格 | 组件 10b | 蓝色表头，隔行 `#F7F8FA` |
| `` `代码` `` | 组件 6e | 行内代码 |
| `![]()` | 组件 12 | 图片容器 |
| 文首作者信息 | 删除 | 不生成任何开头署名标签 |
| 文末署名 | 组件 14 | 统一成「—— 李云龙增长研习社」 |
| —— | —— | **不生成导读卡、不生成英文标签、不生成文首署名** |

---

## 深色模式说明（重要，别当成已解决）

微信深色模式不读开发者的媒体查询，它对正文做的是**自动反色重映射**：
背景变深，接近黑色的文字被提亮，而**显式写死的中间调颜色往往被原样保留**。
所以「适配」只能靠选色规避，做不到精确控制。本主题的处理：

**已规避的坑**

- **正文用 `#3F3F3F`**：足够深，会被微信识别为「深色文字」并提亮，不会留在中间调发灰。
  这也是规范里写「不要用纯黑」之外还必须够深的原因——`#666` 以上就危险了。
- **不用彩色底块装文字**：6b 重点加粗是纯橙字、不加底色；引言卡高亮也是橙字不是橙底。
  浅底色块在深色模式下会被压暗，而块内文字颜色被保留，就是「发脏」最常见的成因。
- **`#F7F8FA` 只用于弱区分**：引用块、卡片的可读性由左边框和文字本身承担，
  不依赖底色对比。底色被压暗后，块内 `#3F3F3F` 会跟着被提亮，仍然可读。
- **橙色 `#FF6B35` 是两种模式下都安全的色**：在白底和深底上对比度都够，
  所以重点、下划线、数据标注全部押在橙上，而不是押在蓝上。
- **去掉英文标签和文首署名标签，是两处意外收益**：
  英文标签原来用 `#8C8C8C`，正是深色模式下最容易发脏的色；
  署名标签是白字压橙底，对比度只有约 2.6:1，本来就低于 WCAG AA。
  这两处现在都不存在了，风险面比第一版小。

**仍有风险的地方**

- **`#8C8C8C` 次要文字**：正处在中间调，深色模式下可能既不提亮也不压暗，
  是最容易「发脏」的一处。现在它只剩图注、来源、指标名、文末署名这几处，
  都属于**丢了也不影响理解**的位置，正文信息一律不用它。
- **`#123A66` 标题深蓝**：深色模式下会被提亮成浅蓝，观感和浅色模式不同，
  但不影响可读性。介意的话把一级标题改成 `#1B4F8A`，提亮后更接近品牌蓝。
- **表格蓝色表头 + 白字**：表头底色 `#1B4F8A` 会被保留，白字仍可读，风险低。

**必须实测**：以上是基于选色的规避策略，不是保证。
每篇文章发布前，用手机开深色模式预览一次，重点看引用块和数据卡片。
微信的反色策略随版本变化，出问题就调 `#8C8C8C` 那几处。
