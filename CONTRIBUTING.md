# 贡献指南

欢迎对 HCF 派生标注数据集与配套方法提出改进、新增用例与代码提交。

## 1. 提 issue 与讨论

- **报告 bug / 数据错误**：请直接开 issue，标题用 `[在 GitHub 仓库开`r 的 issue 名]` 模板（见 Issue 区）
- **方法质疑**：同样开 issue，附上复现命令 + 结果——我们尊重可复现的质疑
- **征集合作用例**：见置顶 issue `[征集用例 / 合作伙伴]`
- 评论与 issue 须使用中文或英文

## 2. 提 PR（数据 / 文档 / 代码）

1. Fork → 本项目目标
2. 新建分支：`git checkout -b fix/<一句话描述>`
3. 修改并提交：`git commit -m "<一句话描述>"`
4. 推送到你的 Fork：`git push origin fix/<一句话描述>`
5. 开 PR，标题用 `[PR] <一句话描述>`
6. 等待 maintainer review（响应周期：通常 3 个工作日内）

## 3. 数据集（hcf_annotations.csv）提交规则

- 新增案例：在 `cases/<category>/<id>.json` 下提交，每例一个 JSON
- 字段约束见 `cases/README.md`
- 涉及商业因素（合作金额、合同条款）请走邮件，不入公共 issue

## 4. 联系方式

- **作者**：刘翔宇（Xiangyu Liu）
- **机构**：北京源空科技
- **邮箱**：liuxiangyu@liuxiangyu.com.cn
- **GitHub**：[@hololink17](https://github.com/hololink17)