# Student Center 控制台

控制所有 Student Center App（原版、梁钧淘版、正式版）的校历：突发远程日、延迟开学、停课和通知。

- 控制台：`https://henryyang141-crypto.github.io/student-center-admin/admin.html`
- 公开校历：`https://henryyang141-crypto.github.io/student-center-admin/`
- 数据：`calendar.json`（App 读取这个文件）

## 第一次使用

1. 打开 GitHub → Settings → Developer settings → **Fine-grained personal access tokens** → Generate new token。
   - Repository access：Only select repositories → `student-center-admin`
   - Permissions → Repository → **Contents: Read and write**
2. 打开控制台，填入 `henryyang141-crypto/student-center-admin` 和令牌，点“连接并读取”。令牌只保存在这台电脑的浏览器里，不会上传。

## 突发远程日（例如天气）

1. 第 3 区选日期，模板选“远程教学日”，按通知改每节时间、取消的节次和原因。
2. 勾选“同时给所有人发通知”，点“添加这一天”。
3. 点“发布到所有 App”。

当天每个学生自己的第 N 节课会自动套用新的第 N 节时间；上课提醒、实时活动、小组件一起更新。

## 什么时候能收到

| 情况 | 生效时间 |
|---|---|
| 打开 App / 回到 App | 几秒内（最多约 5 分钟 CDN 缓存） |
| App 在后台 | 由 iOS 安排，通常几十分钟内 |
| 很久没打开 App | 下次打开时 |

通知是 App 拉取到新内容后在手机本地发出的，不需要服务器，也不收集任何学生数据。

## 以后：秒级推送（需要付费开发者账号）

真正的“点一下所有手机立刻响”需要 Apple 推送服务（APNs），只有 $99/年的 Apple Developer Program 才能用。开通后：

1. 在 Apple Developer 生成 APNs Auth Key（.p8），在 Firebase 建项目并上传这个 Key。
2. App 加入 Firebase Messaging，启动时订阅主题 `student-center`。
3. 在这个仓库的 Settings → Secrets 添加 `FCM_SERVICE_ACCOUNT`，再加一个 workflow：`calendar.json` 有新通知时调用 FCM 发到主题 `student-center`。

在那之前，现在的方式不用改，以后加上推送也会继续工作。
