#!/usr/bin/env python3
"""Builds privacy/*.html: one privacy policy per Student Center edition.

Run from the repository root:  python3 scripts/build_privacy.py
Edit the text here, not the generated pages.
"""
from pathlib import Path

UPDATED_ZH = "2026 年 11 月 7 日"
UPDATED_EN = "November 7, 2026"
CONTACT = "https://github.com/henryyang141-crypto/student-center-admin/issues"
BASE = "https://henryyang141-crypto.github.io/student-center-admin/privacy/"

EDITIONS = {
    "original": dict(
        zh="原版", en="Original edition", app="Student Center", bundle="com.henryyang.studentcenter",
        dist_zh="开发者本人用 Xcode 直接安装到自己的 iPhone，不上架、不对外分发。",
        dist_en="Installed by the developer on his own iPhone with Xcode. Not on the App Store and not distributed.",
        who_zh="开发者本人（Henry）", who_en="the developer (Henry) himself",
        builtin=True, jupiter="full", classroom="web+api", doe=False, testflight=False, appstore=False),
    "juntao": dict(
        zh="梁钧淘特别版", en="Liang Juntao edition", app="Student Center 梁钧淘特别版", bundle="com.studentcenter.juntaoliang",
        dist_zh="为梁钧淘个人定制，由开发者用 Xcode 安装到他的设备或模拟器，不上架、不对外分发。",
        dist_en="Made for Liang Juntao personally and installed with Xcode on his device or a simulator. Not on the App Store and not distributed.",
        who_zh="梁钧淘本人", who_en="Liang Juntao himself",
        builtin=True, jupiter="full", classroom="web+api", doe=False, testflight=False, appstore=False),
    "appstore": dict(
        zh="正式版（App Store 版）", en="App Store edition", app="Student Center", bundle="com.henryyang.studentcenter.formal",
        dist_zh="通过 Apple App Store 公开发布。为了符合 App Store 审核规则，这个版本对 Jupiter 和 Google Classroom 的功能做了限制（见下文）。",
        dist_en="Published on the Apple App Store. To follow App Store rules, this edition limits what it does with Jupiter and Google Classroom (see below).",
        who_zh="安装它的学生", who_en="the student who installs it",
        builtin=False, jupiter="manual", classroom="api", doe=True, testflight=False, appstore=True),
    "testflight": dict(
        zh="满血正式版（TestFlight 版）", en="Full edition (TestFlight)", app="SC 满血版", bundle="com.henryyang.studentcenter.full",
        dist_zh="只通过 Apple TestFlight 发给受邀的测试者，不在 App Store 上架。它在正式版的基础上恢复了 Jupiter 自动同步和 Google Classroom 网页登录，所以风险也更高，请完整阅读第 5–7 节。",
        dist_en="Shared only through Apple TestFlight with invited testers; it is not on the App Store. It adds back Jupiter auto-sync and Google Classroom web sign-in on top of the App Store edition, so it carries more risk. Please read sections 5–7 in full.",
        who_zh="受邀的测试者", who_en="invited testers",
        builtin=False, jupiter="full", classroom="web+api", doe=True, testflight=True, appstore=False),
}


def e(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------- Chinese

def zh(ed):
    full = ed["jupiter"] == "full"
    web = "web" in ed["classroom"]
    out = []
    S = out.append

    S('<div class="alert"><h3>请先读这三条</h3><ol>'
      '<li><b>不要反复点“读取成绩”或“同步”。</b>每点一次，App 都会在 Jupiter 上把你每一门课的页面打开一遍（Classroom 网页同步会打开 3 个作业页面）。'
      '连续快速地点，在学校系统看来像是机器人在批量抓取，可能触发限速、账号被临时锁定，甚至让学校 IT 来问你。App 已经限制 1 分钟内只能手动同步一次，但请你自己也不要反复点。</li>'
      '<li><b>这是非官方工具。</b>Jupiter 和 Google Classroom 都没有授权这个 App 读取你的网页内容。'
      + ("这个版本会在后台自动登录并读取，" if full else "")
      + '学校、NYC DOE、Jupiter 或 Google 都可能认为这违反他们的使用条款。使用它的风险由你自己承担。</li>'
      '<li><b>一切以官方为准。</b>App 里的成绩、GPA、作业截止时间都是从网页上读出来再计算的，可能不完整、过时或算错。重要的事（成绩申诉、截止时间、毕业学分）请务必去 Jupiter、Google Classroom 官方页面或问老师核对。</li>'
      '</ol></div>')

    S('<h2 id="z1">1. 这个版本是什么</h2>')
    S(f'<p>本政策只适用于 <b>{ed["app"]}</b>（{ed["zh"]}，Bundle ID <code>{ed["bundle"]}</code>）。{ed["dist_zh"]}</p>')
    S('<p>Student Center 是一个学生自己开发的个人学习规划 App，<b>与纽约市公立学校（NYC DOE / NYCPS）、Bayside High School、Jupiter（Jupiter Ed）、Clever、Google 都没有任何关联</b>，也没有得到它们的认可或授权。其他版本有各自的隐私政策，见页面底部。</p>')

    S('<h2 id="z2">2. 简短版</h2>')
    S(ul([
        "<b>开发者没有服务器，收不到你的任何个人信息。</b>你的资料、课表、成绩、作业都只保存在你自己的 iPhone 上。",
        "<b>没有广告、没有统计分析、没有追踪、不卖数据。</b>App 里没有任何第三方统计或广告 SDK。",
        "<b>密码在学校或 Google 自己的网页上输入。</b>App 的代码不读取、不保存你的密码。",
        "App 会联网的地方只有：你选择连接的 Jupiter / Clever / NYCENET、Google、" + ("NYC DOE Student Documents、" if ed["doe"] else "") + "以及读取学校校历的 GitHub。详见第 4 节。",
        ("<b>这个版本会保存登录状态并在后台自动同步</b>，便利性最高，风险也最高。详见第 5、6 节。" if full else
         "<b>这个版本不会在后台访问 Jupiter，不会替你登录，不会保存密码。</b>"),
    ]))

    S('<h2 id="z3">3. 保存在你手机上的数据</h2>')
    rows = []
    if ed["builtin"]:
        rows.append([f"姓名、学号、照片、课表等个人资料", f"这个版本为{ed['who_zh']}预先写在 App 里，也可以在 App 里修改", "显示学生卡、今天的课、实时活动和小组件", "App 内、钥匙串"])
    else:
        rows.append(["姓名、学校、OSIS 号、条形码、照片", "你自己输入、扫描学生卡或从相册选择", "显示学生卡、个性化界面", "App 内、钥匙串"])
        rows.append(["课表（课程、老师、教室）", "你自己输入，或导入 Program Card PDF / 照片", "今天的课、实时活动、小组件、上课提醒", "App 内、钥匙串"])
    rows += [
        ["作业", "你自己添加，或从 Google Classroom 导入", "待办清单、优先级评分", "App 内"],
        ["成绩、作业明细", "你自己输入，或从 Jupiter 读取", "GPA、What-if 计算、毕业进度、新成绩提醒", "App 内"],
        ["毕业学分、Regents 成绩", "你自己输入", "毕业进度", "App 内"],
    ]
    if full:
        rows.append(["Jupiter / Clever / NYCENET 的登录 Cookie（登录状态）", "你登录后由 App 复制一份", "App 重启后不用重新登录、后台自动同步", "钥匙串（仅本机，首次解锁后可读）"])
        if web:
            rows.append(["Google 的登录 Cookie", "你在 Classroom 网页登录后由 App 复制一份", "自动读取 Classroom 作业", "钥匙串（仅本机，首次解锁后可读）"])
    if "api" in ed["classroom"]:
        rows.append(["Google 授权令牌（只读）", "你在 Google 授权页同意后获得", "通过 Google 官方接口读取 Classroom", "钥匙串"])
    rows += [
        ["网站数据（Cookie、缓存）", "App 内浏览器（Apple WebKit）像 Safari 一样自动保存", "网站记住你的登录", "App 的网页数据目录"],
        ["学校校历缓存", "从 GitHub 下载", "特殊课表日、停课、学校通知", "钥匙串（与小组件共享）"],
        ["设置（语言、提醒、目标等）", "你的选择", "记住你的偏好", "App 内"],
    ]
    S(table(["数据", "从哪里来", "用来做什么", "存在哪里"], rows))
    S('<p>这些数据不会上传给开发者。小组件和实时活动只读取同一台手机上的这些数据。</p>')

    S('<h2 id="z4">4. App 会和哪些网站通信</h2>')
    rows = [
        ["GitHub（api.github.com、raw.githubusercontent.com、github.io）", "打开 App 时、以及 iOS 安排的后台刷新", "只下载公开的校历文件 <code>calendar.json</code>。不发送任何学生信息。GitHub 会像所有网站一样看到你的 IP 地址和设备类型，受 GitHub 隐私声明约束。"],
        ["Jupiter、Clever、NYCENET（NYC DOE 登录）",
         "你连接 Jupiter 后；" + ("打开 App（最多每 10 分钟一次）、下拉刷新、点“立即同步”、以及 iOS 安排的后台刷新" if full else "你打开 Jupiter 页面、点“读取成绩”、打开成绩页（最多每 15 分钟一次）或下拉刷新时"),
         "像普通浏览器一样加载网页，网站会看到你的账号、IP 和浏览器标识。为了得到电脑版成绩表，App 内浏览器会以<b>“Mac 上的 Safari”</b>身份访问。"],
        ["Google（accounts.google.com、classroom.google.com、Classroom API）",
         "你连接 Google Classroom 后" + ("；网页登录模式下打开 App（最多每 10 分钟一次）和下拉刷新时也会自动读取" if web else "，打开作业页或下拉刷新时"),
         "Google 会看到你的账号和 IP。" + ("网页登录模式也会以“Mac 上的 Safari”身份访问。" if web else "")],
    ]
    if ed["doe"]:
        rows.append(["NYC DOE Student Documents", "只在你选择导入 Program Card 时", "在私密的 App 内浏览器中打开，关闭后登录状态结束；App 只在本机读取你打开的 PDF。"])
    if ed["testflight"]:
        rows.append(["Apple TestFlight", "安装和使用测试版时", "见第 11 节。"])
    if ed["appstore"]:
        rows.append(["Apple App Store", "下载和更新时", "由 Apple 处理，受 Apple 隐私政策约束。如果你在 iPhone 设置里选择“与 App 开发者共享”，开发者可能看到匿名的崩溃报告和使用统计。"])
    S(table(["网站", "什么时候", "会发生什么"], rows))

    # ---------------- Jupiter
    S('<h2 id="z5">5. Jupiter 成绩：怎么运作，有哪些风险</h2>')
    if full:
        S('<h3>这个版本怎么做</h3>')
        S(ul([
            "你点“连接 Jupiter 自动同步成绩”，在 Clever / NYCENET 自己的登录页上输入账号密码。App 的代码不读取密码。",
            "登录成功后，App <b>把 Jupiter、Clever、NYCENET 的登录 Cookie 复制一份存进 iOS 钥匙串</b>，这样 App 被关掉后也不用重新登录。",
            "之后 App 会在一个看不见的内置浏览器里打开 Jupiter，逐门课读取成绩和作业明细：打开 App 时（距离上次至少 10 分钟）、下拉刷新、点“立即同步”时，以及 iOS 安排的后台刷新（大约每 30 分钟最多一次，具体由 iOS 决定）。",
            "如果登录过期，App 会重新打开 Clever 的入口，<b>并自动点一下 Clever 页面上的“NYCENET”登录按钮</b>，让还有效的学校登录自动接上。它不会输入密码；如果需要密码，App 会停下来并通知你自己登录。",
            "出现新成绩或分数变化时，App 在手机本地发通知，通知里会显示课程名、作业名和分数。",
        ]))
    else:
        S('<h3>这个版本怎么做</h3>')
        S(ul([
            "你点“打开 Jupiter 读取成绩”，在 Clever / NYCENET 自己的登录页上自己登录。App 不会替你填写或点击任何登录内容。",
            "进入 Jupiter 成绩页后，只有你点“读取成绩”，App 才会逐门课读取成绩和作业明细，过程中页面会在你眼前翻动。",
            "读取过一次后，你每次打开成绩页（距离上次至少 15 分钟）或下拉刷新时，如果 App 内的 Jupiter 仍在登录状态，App 会在后面重新加载一次 Jupiter 并更新成绩。登录过期就停下来，请你自己重新登录。",
            "<b>App 不在后台访问 Jupiter，不自动登录，不额外复制或保存密码、Cookie。</b>App 内浏览器（Apple WebKit）会像 Safari 一样自己保存网站 Cookie。",
        ]))
    S('<h3>风险点（请认真看）</h3>')
    risks = [
        "<b>没有官方授权。</b>Jupiter 没有给学生用的公开接口，这个 App 是读取你能看到的网页。Jupiter、Clever 或 NYC DOE 的使用条款、学校的电脑使用规定（Acceptable Use Policy）可能不允许用自动化工具访问。如果他们认为你违规，可能限制访问、锁定账号或要求你说明情况。",
        "<b>可能被当成机器人。</b>每次同步都会连续打开你所有课的页面。频繁同步、反复点按，或很多学生同时用，会产生异常流量，可能触发网站的限速或安全检查。",
        "<b>成绩可能不准。</b>Jupiter 一改网页，读取就可能失败、漏掉课程或读错数字。App 里的 GPA 是按 App 自己的规则估算的，<b>不是官方成绩单</b>，不能用来申诉或申请。",
        "<b>浏览器标识。</b>为了拿到电脑版成绩表，App 会以“Mac 上的 Safari”身份访问。学校或 Jupiter 的登录记录里可能显示一台 Mac 在登录你的账号，这是 App 造成的，不是别人盗号——但如果你看到你不认识的登录，仍然应该立刻改密码。",
        "<b>App 内登录页。</b>登录页显示在 App 里的浏览器中，而不是 Safari。技术上，任何 App 都能读取它自己内置浏览器里的内容；这个 App 的代码不读取密码栏。如果你不放心，就不要连接，手动输入成绩即可。",
    ]
    if full:
        risks += [
            "<b>登录状态存在手机里。</b>谁能解锁并打开你的手机和这个 App，谁就能看到你的成绩，甚至用 App 内浏览器进入你的 Jupiter。请开启 Face ID 保护，不要把手机借给别人用这个 App。",
            "<b>自动点击 NYCENET 按钮</b>属于自动化操作。它不输入密码，但仍然是“机器在替你点”。",
            "<b>后台同步</b>由 iOS 决定时间，不保证实时，也可能消耗少量电量和流量。",
            "<b>手机丢了怎么办：</b>立刻在电脑上修改 NYCDOE 账号密码，这会让手机里保存的登录状态失效。",
        ]
    S(ul(risks))

    # ---------------- Classroom
    S('<h2 id="z6">6. Google Classroom 作业：怎么运作，有哪些风险</h2>')
    if web:
        S('<p>这个版本有两种连接方式，在“作业”页点 Classroom 卡片选择：</p>')
        S('<h3>方式 A：网页登录（默认）</h3>')
        S(ul([
            "你在 Google 自己的登录页登录 classroom.google.com。App 把 Google 的登录 Cookie 复制一份存进钥匙串。",
            "之后 App 在看不见的内置浏览器里打开 Classroom 的“待办”页面（已分配、缺交、已上交 3 个页面），读取作业标题、课程、截止时间和链接。打开 App（距离上次至少 10 分钟）、下拉刷新时会自动读取。",
            "只读，不会提交、修改或删除 Classroom 里的任何内容。",
        ]))
        S('<p><b>网页登录的风险：</b></p>')
        S(ul([
            "<b>不是 Google 提供的方式。</b>Google 服务条款不允许用非 Google 提供的方式自动访问其服务。Google 可能要求你重新验证身份、结束登录，或者认为这是可疑活动。",
            "<b>学校的 Google Workspace 管理员可以看到登录记录。</b>记录里会显示“Mac 上的 Safari”。学校可能禁止或调查这类登录。",
            "<b>登录 Cookie 存在手机里</b>，风险和第 5 节一样：能打开你手机和 App 的人能看到你的作业，App 内浏览器也带着你的 Google 登录。",
            "<b>截止时间是推算的。</b>Classroom 网页不显示年份，App 会按今天的日期推算，可能差一年或差几个小时。",
            "Google 改网页后读取可能失败或漏掉作业。",
        ]))
        S('<h3>方式 B：Google 授权</h3>')
    S(ul([
        "通过 Google 官方授权页，经你同意后，App 获得<b>只读</b>权限：课程列表、作业、你的提交状态。令牌存在钥匙串里，App 只从你的手机直接访问 Google。",
        "对 Google API 数据的使用遵守 <a href=\"https://developers.google.com/terms/api-services-user-data-policy\">Google API Services User Data Policy</a>，包括 Limited Use（有限使用）要求：数据只用于在你手机上显示你的作业，不转给任何人，不用于广告。",
        "<b>风险：</b>这个 App 不是 Google 审核过的 App，Google 可能显示“未经验证的应用”警告；很多学校的管理员会直接阻止它，这时请改用手动添加作业" + ("或网页登录" if web else "") + "。你可以随时在 App 内“移除本机授权”，或在 <a href=\"https://myaccount.google.com/permissions\">myaccount.google.com/permissions</a> 撤销。",
    ]))

    # ---------------- repeated taps
    S('<h2 id="z7">7. 为什么不要反复点“读取成绩” / “同步”</h2>')
    S('<p>这一节专门说清楚，因为这是最容易出问题的地方。</p>')
    S(ul([
        "<b>一次读取 = 很多次访问。</b>读取成绩时，App 会把 Jupiter 上你的每一门课、每个 Quarter 的页面挨个打开。如果你有 8 门课，一次读取就是几十次页面访问。Classroom 网页同步每次会打开 3 个页面并滚动加载。",
        "<b>连续快速点按看起来就像攻击或抓取程序。</b>网站可能因此限速、弹出验证、临时锁定账号，学校 IT 也可能注意到异常。",
        "<b>不会让成绩更新得更快。</b>老师录入成绩后 Jupiter 才会有，反复点只会读到同样的内容。",
        "<b>App 已经做的保护：</b>" + ("两次手动同步至少间隔 1 分钟（1 分钟内再点会提示你稍后再试）；打开 App 自动同步至少间隔 10 分钟；后台刷新由 iOS 安排，大约最多每 30 分钟一次；Classroom 网页同步也至少间隔 1 分钟。" if full else
                                     "两次读取至少间隔 1 分钟（1 分钟内再点会提示你稍后再试）；打开成绩页自动更新至少间隔 15 分钟；不在后台运行。"),
        "<b>正确做法：</b>正常情况下根本不用点，打开 App 就会自动更新。读取失败时，先等几分钟，去 Jupiter 官方网页确认能否正常打开；还不行就点“重新登录”，<b>不要连续重试</b>。看到“登录已过期”时，自己重新登录一次即可。",
    ]))

    S('<h2 id="z8">8. 通知、锁屏和共享设备</h2>')
    S(ul([
        "通知全部由手机本地发出，不经过任何服务器。" + ("新成绩通知会显示课程、作业和分数，" if full else "") + "学校通知（远程日、停课等）来自 GitHub 上的公开校历。",
        ("锁屏上的通知可能被旁人看到。不想让别人看到分数，可以在 iPhone“设置 › 通知 › " + ed["app"] + " › 显示预览”里选“解锁时”或“从不”。" if full else "学校通知会显示在锁屏上；可以在 iPhone 的通知设置里关闭预览。"),
        "实时活动和小组件会在锁屏/主屏显示今天的课程和作业。",
        "不要在借来的、共用的或学校的设备上使用这个 App 连接你的账号。",
    ]))

    S('<h2 id="z9">9. Face ID、相机、相册和 AI</h2>')
    S(ul([
        "Face ID / 密码完全由 iOS 处理，App 只知道“验证成功或失败”。",
        "相机和相册只在你主动扫描学生卡、课表或选择照片时使用，图片只在本机识别。",
        "作业优先级的 AI 评分使用 Apple 的本机模型（如果设备支持）或简单规则，不发送到任何服务器。",
    ]))

    S('<h2 id="z10">10. 未成年人</h2>')
    S('<p>Student Center 为高中生设计，不面向 13 岁以下儿童。App 不收集任何人的个人信息。如果你未满 18 岁，建议在家长或监护人知情的情况下连接学校账号，并一起阅读第 5–7 节的风险。</p>')

    if ed["testflight"]:
        S('<h2 id="z11">11. TestFlight 测试版说明</h2>')
        S(ul([
            "这个版本只通过 Apple TestFlight 分发。你需要安装 Apple 的 TestFlight App。TestFlight 本身由 Apple 运营，受 <a href=\"https://www.apple.com/legal/privacy/\">Apple 隐私政策</a>和 TestFlight 条款约束。",
            "按 TestFlight 的规则，开发者在 App Store Connect 里可能看到：你被邀请时使用的邮箱和名字（通过公开链接加入则不显示邮箱）、安装日期、设备型号、iOS 版本、测试版本号，以及你<b>主动提交</b>的反馈、截图和崩溃报告。开发者只用这些信息修复问题，不会公开或转给他人。",
            "测试版可能有 Bug，每个版本 90 天后会过期，需要更新到新的测试版。",
            "测试版功能（Jupiter 自动同步、Classroom 网页登录）可能随时被修改或移除，尤其是当学校、Jupiter、Google 或 Apple 提出要求时。",
        ]))
    n = 12 if ed["testflight"] else 11
    S(f'<h2 id="z{n}">{n}. 怎样删除你的数据</h2>')
    steps = []
    if full:
        steps.append("在“成绩”页点“断开 Jupiter”：删除本机读取的成绩、App 内的 Jupiter 网站数据和钥匙串里的登录 Cookie。")
    else:
        steps.append("在“成绩”页点“删除读取的成绩”：删除本机读取的成绩并退出 App 内的 Jupiter 登录。")
    if web:
        steps.append("在“作业” › Classroom 里点“退出网页登录”：删除 Google 网站数据和钥匙串里的 Google Cookie（已导入的作业会保留，可以手动删除）。")
    if "api" in ed["classroom"]:
        steps.append("在“作业” › Classroom 里“移除本机授权”，并可在 myaccount.google.com/permissions 撤销。")
    steps.append("其他资料可以在 App 内逐项编辑或删除。")
    steps.append("<b>先做完上面几步再删除 App。</b>iOS 有时会在删除 App 后继续保留钥匙串里的内容，所以登录状态最好在 App 内先清除。")
    S("<ol>" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>")
    n += 1
    S(f'<h2 id="z{n}">{n}. 免责声明</h2>')
    S('<p>App 按“现状”提供，不保证读取到的成绩、作业、课表和校历完整、准确或及时，也不保证与 Jupiter、Clever、NYCENET、Google 的连接一直可用。因使用 App 连接学校或 Google 账号产生的后果（包括账号受限、违反学校规定等）由使用者自行承担。所有成绩、截止时间、毕业要求请以学校和官方系统为准。</p>')
    n += 1
    S(f'<h2 id="z{n}">{n}. 政策变更和联系方式</h2>')
    S(f'<p>如果本政策有变化，新版本会发布在这个网址并更新日期；重大变化会在 App 内或校历通知中提示。有问题请在 <a href="{CONTACT}">GitHub Issues</a> 留言（不要在留言里写你的密码、学号或成绩）。</p>')
    return "\n".join(out)


# ---------------------------------------------------------------- English

def en(ed):
    full = ed["jupiter"] == "full"
    web = "web" in ed["classroom"]
    out = []
    S = out.append
    S('<div class="alert"><h3>Read these three first</h3><ol>'
      '<li><b>Don’t tap “Read grades” or “Sync” over and over.</b> Each tap makes the app open the page of every one of your classes on Jupiter (a Classroom web sync opens 3 assignment pages). '
      'Rapid repeated taps look like a bot to the school’s systems and can trigger rate limits, a temporary account lock, or questions from school IT. The app already allows only one manual sync per minute, but please don’t keep tapping.</li>'
      '<li><b>This is an unofficial tool.</b> Neither Jupiter nor Google has authorized this app to read your pages. '
      + ("This edition signs back in and reads in the background. " if full else "")
      + 'Your school, NYC DOE, Jupiter or Google may consider this against their terms. You use it at your own risk.</li>'
      '<li><b>The official systems are the source of truth.</b> Grades, GPA and due dates in the app are read from web pages and calculated, and can be incomplete, out of date or wrong. Check anything important on Jupiter, Google Classroom or with your teacher.</li>'
      '</ol></div>')
    S('<h2 id="e1">1. Which app this covers</h2>')
    S(f'<p>This policy covers only <b>{ed["app"]}</b> ({ed["en"]}, bundle ID <code>{ed["bundle"]}</code>). {ed["dist_en"]}</p>')
    S('<p>Student Center is a personal school planner built by a student. It is <b>not affiliated with, endorsed by, or authorized by</b> NYC Public Schools (NYC DOE), Bayside High School, Jupiter (Jupiter Ed), Clever or Google. Other editions have their own policies, linked at the bottom of this page.</p>')
    S('<h2 id="e2">2. The short version</h2>')
    S(ul([
        "<b>The developer runs no server and receives none of your information.</b> Your profile, schedule, grades and assignments stay on your iPhone.",
        "<b>No ads, no analytics, no tracking, no selling data.</b> The app contains no third-party analytics or ad SDKs.",
        "<b>You type passwords on your school’s or Google’s own pages.</b> The app’s code doesn’t read or store them.",
        "The app only talks to the services you connect (Jupiter / Clever / NYCENET, Google" + (", NYC DOE Student Documents" if ed["doe"] else "") + ") and GitHub for the school calendar. See section 4.",
        ("<b>This edition keeps your sign-ins and syncs in the background.</b> It is the most convenient and the most risky. See sections 5 and 6." if full else
         "<b>This edition never visits Jupiter in the background, never signs in for you, and never stores your password.</b>"),
    ]))
    S('<h2 id="e3">3. Data stored on your iPhone</h2>')
    rows = []
    if ed["builtin"]:
        rows.append(["Name, ID number, photo, schedule", f"Built into this edition for {ed['who_en']}; editable in the app", "Student card, today’s classes, Live Activity, widgets", "App storage, Keychain"])
    else:
        rows.append(["Name, school, OSIS number, barcode, photo", "You type, scan your ID, or pick a photo", "Student card, personalization", "App storage, Keychain"])
        rows.append(["Class schedule", "You type it, or import a Program Card PDF / photo", "Today’s classes, Live Activity, widgets, reminders", "App storage, Keychain"])
    rows += [
        ["Assignments", "You add them, or import from Google Classroom", "To-do list, priority ratings", "App storage"],
        ["Grades and assignment details", "You type them, or read them from Jupiter", "GPA, what-if, graduation progress, new-grade alerts", "App storage"],
        ["Credits and Regents scores", "You type them", "Graduation progress", "App storage"],
    ]
    if full:
        rows.append(["Jupiter / Clever / NYCENET sign-in cookies", "Copied by the app after you sign in", "Stay signed in after relaunch; background sync", "Keychain (this device only, readable after first unlock)"])
        if web:
            rows.append(["Google sign-in cookies", "Copied by the app after you sign in to Classroom on the web", "Automatic Classroom reads", "Keychain (this device only, readable after first unlock)"])
    if "api" in ed["classroom"]:
        rows.append(["Google authorization token (read-only)", "Granted by you on Google’s consent page", "Reading Classroom through Google’s official API", "Keychain"])
    rows += [
        ["Website data (cookies, cache)", "Kept by the in-app browser (Apple WebKit), like Safari", "Sites remember your sign-in", "App’s web data folder"],
        ["School calendar cache", "Downloaded from GitHub", "Special bell days, closures, school notices", "Keychain (shared with widgets)"],
        ["Settings", "Your choices", "Remember your preferences", "App storage"],
    ]
    S(table(["Data", "Source", "Purpose", "Where"], rows))
    S('<p>None of this is sent to the developer. Widgets and the Live Activity read the same data on the same phone.</p>')
    S('<h2 id="e4">4. Network connections</h2>')
    rows = [
        ["GitHub (api.github.com, raw.githubusercontent.com, github.io)", "When you open the app and during background refresh scheduled by iOS", "Downloads the public <code>calendar.json</code> only. No student information is sent. Like any website, GitHub sees your IP address and device type under GitHub’s privacy statement."],
        ["Jupiter, Clever, NYCENET (NYC DOE sign-in)",
         "After you connect Jupiter: " + ("when the app opens (at most every 10 minutes), on pull-to-refresh or “Sync now”, and during iOS background refresh" if full else "when you open Jupiter, tap “Read grades”, open Grades (at most every 15 minutes) or pull to refresh"),
         "Pages load like in any browser; the sites see your account, IP and browser. To get the desktop grade tables, the in-app browser identifies itself as <b>Safari on a Mac</b>."],
        ["Google (accounts.google.com, classroom.google.com, Classroom API)",
         "After you connect Classroom" + ("; in web sign-in mode also when the app opens (at most every 10 minutes) and on pull-to-refresh" if web else ", when you open Assignments or pull to refresh"),
         "Google sees your account and IP." + (" Web sign-in mode also identifies as Safari on a Mac." if web else "")],
    ]
    if ed["doe"]:
        rows.append(["NYC DOE Student Documents", "Only when you choose to import your Program Card", "Opens in a private in-app browser whose session ends when closed; the app reads the PDF you open on the device."])
    if ed["testflight"]:
        rows.append(["Apple TestFlight", "Installing and using the beta", "See section 11."])
    if ed["appstore"]:
        rows.append(["Apple App Store", "Download and updates", "Handled by Apple under Apple’s privacy policy. If you turn on “Share with App Developers” in iPhone Settings, the developer may see anonymous crash reports and usage statistics."])
    S(table(["Service", "When", "What happens"], rows))

    S('<h2 id="e5">5. Jupiter grades: how it works and the risks</h2>')
    S('<h3>What this edition does</h3>')
    if full:
        S(ul([
            "You tap “Connect Jupiter” and sign in on Clever / NYCENET’s own pages. The app’s code doesn’t read your password.",
            "After sign-in, the app <b>copies the Jupiter, Clever and NYCENET sign-in cookies into the iOS Keychain</b> so you stay signed in after the app is closed.",
            "The app then opens Jupiter in a hidden in-app browser and reads each class’s grades and assignments: when the app opens (at least 10 minutes after the last sync), on pull-to-refresh or “Sync now”, and in iOS background refresh (roughly at most every 30 minutes, timing decided by iOS).",
            "If the session has ended, the app reopens Clever <b>and automatically taps the “NYCENET” button on Clever’s page</b> so a still-valid school sign-in reconnects. It never types a password; if one is needed it stops and notifies you to sign in yourself.",
            "For new or changed grades, the app posts a local notification showing the class, assignment and score.",
        ]))
    else:
        S(ul([
            "You tap “Open Jupiter to read grades” and sign in yourself on Clever / NYCENET’s pages. The app never fills in or taps anything on a sign-in page.",
            "Once you’re on your Jupiter grades, the app reads each class’s grades only when you tap “Read grades”, with the pages changing in front of you.",
            "After the first read, opening Grades (at least 15 minutes after the last read) or pulling to refresh reloads Jupiter behind the screen and updates grades, as long as Jupiter is still signed in inside the app. If the session ended, it stops and asks you to sign in again.",
            "<b>The app never visits Jupiter in the background, never signs in for you, and makes no extra copy of passwords or cookies.</b> The in-app browser (Apple WebKit) keeps website cookies itself, like Safari.",
        ]))
    S('<h3>Risks (please read)</h3>')
    risks = [
        "<b>Not authorized.</b> Jupiter offers students no public API; the app reads the web pages you can see. Jupiter’s, Clever’s or NYC DOE’s terms and your school’s Acceptable Use Policy may not allow automated access. If they decide you broke the rules they may restrict access, lock the account or ask you to explain.",
        "<b>It can look like a bot.</b> Each sync opens all your class pages in a row. Frequent syncs, repeated taps, or many students using it at once create unusual traffic that can trigger rate limits or security checks.",
        "<b>Grades can be wrong.</b> If Jupiter changes its pages, reading can fail, skip classes or misread numbers. The app’s GPA is its own estimate, <b>not an official transcript</b>, and can’t be used for appeals or applications.",
        "<b>Browser identity.</b> To get the desktop tables the app identifies as Safari on a Mac, so school or Jupiter sign-in records may show a Mac signing in to your account. That is the app, not an intruder — but if you see a sign-in you don’t recognize, change your password right away.",
        "<b>In-app sign-in page.</b> The sign-in page appears inside the app’s browser, not Safari. Technically any app can read its own in-app browser; this app’s code doesn’t read password fields. If you’re not comfortable with that, don’t connect and type grades in yourself.",
    ]
    if full:
        risks += [
            "<b>Your sign-in lives on the phone.</b> Anyone who can unlock your phone and open the app can see your grades and even open your Jupiter in the in-app browser. Turn on Face ID protection and don’t lend the phone to others to use this app.",
            "<b>Tapping the NYCENET button automatically</b> is an automated action. It doesn’t enter a password, but it is still the app clicking for you.",
            "<b>Background sync</b> runs when iOS decides, isn’t real time, and uses a little battery and data.",
            "<b>If you lose your phone,</b> change your NYCDOE password from a computer right away; that ends the sign-in stored on the phone.",
        ]
    S(ul(risks))

    S('<h2 id="e6">6. Google Classroom: how it works and the risks</h2>')
    if web:
        S('<p>This edition has two ways to connect; choose one by tapping the Classroom card on Assignments.</p>')
        S('<h3>Option A: Web sign-in (default)</h3>')
        S(ul([
            "You sign in to classroom.google.com on Google’s own page. The app copies Google’s sign-in cookies into the Keychain.",
            "The app then opens Classroom’s To-do pages (Assigned, Missing, Done) in a hidden in-app browser and reads assignment titles, classes, due dates and links: when the app opens (at least 10 minutes after the last read) and on pull-to-refresh.",
            "Read-only: it never turns in, edits or deletes anything in Classroom.",
        ]))
        S('<p><b>Risks of web sign-in:</b></p>')
        S(ul([
            "<b>Not a Google-provided method.</b> Google’s Terms of Service don’t allow accessing its services by automated means other than the ones Google provides. Google may ask you to verify, end the session, or flag it as suspicious.",
            "<b>Your school’s Google Workspace admin can see sign-in records,</b> which will show Safari on a Mac. Your school may block or look into these sign-ins.",
            "<b>Sign-in cookies live on the phone,</b> with the same risks as section 5: anyone who can open your phone and the app can see your work, and the in-app browser carries your Google sign-in.",
            "<b>Due dates are inferred.</b> Classroom’s pages don’t show the year, so the app guesses from today’s date and can be off by a year or a few hours.",
            "If Google changes its pages, reading may fail or miss assignments.",
        ]))
        S('<h3>Option B: Google authorization</h3>')
    S(ul([
        "Through Google’s official consent page, and only with your agreement, the app gets <b>read-only</b> access to your courses, coursework and your submission status. The token is kept in the Keychain and used only from your phone directly to Google.",
        "Use of information received from Google APIs adheres to the <a href=\"https://developers.google.com/terms/api-services-user-data-policy\">Google API Services User Data Policy</a>, including the Limited Use requirements: the data is only shown to you on your phone, never shared, and never used for ads.",
        "<b>Risks:</b> this app is not verified by Google, so Google may show an “unverified app” warning, and many schools block it outright; then add assignments yourself" + (" or use web sign-in" if web else "") + ". You can “Remove local authorization” in the app at any time or revoke it at <a href=\"https://myaccount.google.com/permissions\">myaccount.google.com/permissions</a>.",
    ]))

    S('<h2 id="e7">7. Why you shouldn’t keep tapping “Read grades” / “Sync”</h2>')
    S(ul([
        "<b>One read = many visits.</b> Reading grades opens the page of every class and every quarter on Jupiter, one after another. With 8 classes that is dozens of page loads. A Classroom web sync opens 3 pages and scrolls them.",
        "<b>Rapid repeated taps look like an attack or a scraper.</b> Sites may slow you down, show a challenge or lock the account for a while, and school IT may notice.",
        "<b>It doesn’t make grades appear sooner.</b> Jupiter only has a grade after a teacher enters it; tapping again reads the same thing.",
        "<b>What the app already does:</b> " + ("manual syncs are at least 1 minute apart (tapping sooner shows a reminder); automatic syncs on open are at least 10 minutes apart; background refresh is scheduled by iOS, roughly at most every 30 minutes; Classroom web syncs are also at least 1 minute apart." if full else
                                                 "reads are at least 1 minute apart (tapping sooner shows a reminder); automatic updates on opening Grades are at least 15 minutes apart; nothing runs in the background."),
        "<b>What to do instead:</b> normally you don’t need to tap at all — opening the app updates for you. If a read fails, wait a few minutes and check that the official Jupiter site works; if it still fails, sign in again. <b>Don’t retry in a loop.</b> When it says the session expired, just sign in once yourself.",
    ]))
    S('<h2 id="e8">8. Notifications, Lock Screen and shared devices</h2>')
    S(ul([
        "All notifications are created on the phone; no server is involved. " + ("New-grade notifications show the class, assignment and score. " if full else "") + "School notices (remote days, closures) come from the public calendar on GitHub.",
        ("Lock Screen notifications can be seen by people near you. To hide scores, set iPhone Settings › Notifications › " + ed["app"] + " › Show Previews to “When Unlocked” or “Never”." if full else "School notices can appear on the Lock Screen; you can turn previews off in iPhone notification settings."),
        "The Live Activity and widgets show today’s classes and assignments on the Lock Screen and Home Screen.",
        "Don’t connect your accounts in this app on a borrowed, shared or school device.",
    ]))
    S('<h2 id="e9">9. Face ID, camera, photos and AI</h2>')
    S(ul([
        "Face ID / passcode is handled entirely by iOS; the app only learns whether it succeeded.",
        "The camera and Photos are used only when you choose to scan an ID or schedule or pick a photo, and images are processed on the device.",
        "Assignment priority ratings use Apple’s on-device model (when available) or simple rules. Nothing is sent to a server.",
    ]))
    S('<h2 id="e10">10. Minors</h2>')
    S('<p>Student Center is designed for high school students and is not directed to children under 13. It collects no personal information from anyone. If you are under 18, we suggest connecting school accounts with a parent or guardian aware, and reading sections 5–7 together.</p>')
    if ed["testflight"]:
        S('<h2 id="e11">11. About TestFlight</h2>')
        S(ul([
            "This edition is distributed only through Apple TestFlight, which you install from Apple. TestFlight is operated by Apple under the <a href=\"https://www.apple.com/legal/privacy/\">Apple Privacy Policy</a> and TestFlight terms.",
            "Under TestFlight’s rules the developer may see in App Store Connect: the email and name you were invited with (not shown if you joined through a public link), install date, device model, iOS version, build number, and feedback, screenshots and crash reports <b>you choose to send</b>. The developer uses them only to fix problems and never publishes or shares them.",
            "Beta builds can have bugs and expire after 90 days; you’ll need to update to a newer build.",
            "Beta features (Jupiter auto-sync, Classroom web sign-in) may change or be removed at any time, especially if the school, Jupiter, Google or Apple asks.",
        ]))
    n = 12 if ed["testflight"] else 11
    S(f'<h2 id="e{n}">{n}. Deleting your data</h2>')
    steps = []
    steps.append("On Grades, tap “Disconnect Jupiter”: removes read grades, Jupiter website data and the sign-in cookies in the Keychain." if full else
                 "On Grades, tap “Remove read grades”: removes read grades and signs Jupiter out inside the app.")
    if web:
        steps.append("In Assignments › Classroom, tap “Sign out of web sync”: removes Google website data and the Google cookies in the Keychain (imported assignments stay; delete them yourself if you want).")
    if "api" in ed["classroom"]:
        steps.append("In Assignments › Classroom, tap “Remove local authorization”, and optionally revoke at myaccount.google.com/permissions.")
    steps.append("Edit or delete anything else in the app.")
    steps.append("<b>Do the steps above before deleting the app.</b> iOS can keep Keychain items after an app is deleted, so clear sign-ins inside the app first.")
    S("<ol>" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>")
    n += 1
    S(f'<h2 id="e{n}">{n}. Disclaimer</h2>')
    S('<p>The app is provided “as is”. It doesn’t guarantee that grades, assignments, schedules or calendar data are complete, accurate or current, or that connections to Jupiter, Clever, NYCENET or Google keep working. You are responsible for the consequences of connecting school or Google accounts through the app, including account restrictions or school-policy issues. Rely on your school and the official systems for grades, deadlines and graduation requirements.</p>')
    n += 1
    S(f'<h2 id="e{n}">{n}. Changes and contact</h2>')
    S(f'<p>If this policy changes, the new version is posted at this address with a new date; important changes are announced in the app or the calendar notices. Questions: open an issue on <a href="{CONTACT}">GitHub Issues</a> (never include your password, ID number or grades).</p>')
    return "\n".join(out)


CSS = """
:root{--bg:#fbfbfd;--card:#fff;--ink:#1d1d1f;--muted:#6e6e73;--line:#d2d2d7;--accent:#0066cc;--warn-bg:#fff4e5;--warn-ink:#8a4b00;--warn-line:#ffb340}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#000;--card:#1c1c1e;--ink:#f5f5f7;--muted:#a1a1a6;--line:#38383a;--accent:#2997ff;--warn-bg:#2b1d08;--warn-ink:#ffcc80;--warn-line:#a86400}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Helvetica Neue",sans-serif;-webkit-text-size-adjust:100%}
main{max-width:760px;margin:0 auto;padding:40px 16px 80px}
.eyebrow{color:var(--muted);font-size:14px;font-weight:600;letter-spacing:.02em;margin:0}
h1{font-size:clamp(30px,6vw,44px);line-height:1.1;letter-spacing:-.02em;margin:6px 0 8px}
.meta{color:var(--muted);margin:0 0 20px}
nav.lang{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 28px}
nav.lang a{border:1px solid var(--line);border-radius:999px;padding:6px 14px;text-decoration:none;color:var(--ink);font-size:15px}
h2{font-size:24px;letter-spacing:-.01em;margin:44px 0 10px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:18px;margin:22px 0 6px}
p,li{overflow-wrap:anywhere}
ul,ol{padding-left:22px}li{margin:6px 0}
a{color:var(--accent)}
code{font:14px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:1px 5px}
.alert{background:var(--warn-bg);color:var(--warn-ink);border:1px solid var(--warn-line);border-radius:18px;padding:18px 20px;margin:8px 0 8px}
.alert h3{margin:0 0 4px;font-size:19px}.alert b{color:inherit}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card);margin:12px 0}
table{border-collapse:collapse;width:100%;font-size:15px;min-width:560px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
th{font-weight:600;color:var(--muted);font-size:13px}
tr:last-child td{border-bottom:0}
.lang-section{margin-top:56px}
footer{margin-top:64px;color:var(--muted);font-size:14px;border-top:1px solid var(--line);padding-top:16px}
footer a{margin-right:14px}
"""


def editions_footer(current):
    links = []
    for slug, ed in EDITIONS.items():
        name = f"{ed['zh']} · {ed['en']}"
        links.append(f"<b>{name}</b>" if slug == current else f'<a href="{slug}.html">{name}</a>')
    return "<footer><p>各版本隐私政策 · Policies for each edition</p><p>" + " ".join(links) + '</p><p><a href="index.html">全部版本对比 · Compare editions</a></p></footer>'


def page(slug, ed):
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ed['app']} 隐私政策</title>
<meta name="description" content="{ed['app']}（{ed['zh']}）隐私政策与 Jupiter / Google Classroom 风险说明">
<style>{CSS}</style>
</head>
<body>
<main>
<p class="eyebrow">Student Center · {ed['zh']}</p>
<h1>隐私政策与风险说明</h1>
<p class="meta">{ed['app']} · <code>{ed['bundle']}</code><br>更新日期：{UPDATED_ZH} · Last updated {UPDATED_EN}</p>
<nav class="lang"><a href="#zh">中文</a><a href="#en">English</a><a href="#z5">Jupiter 风险</a><a href="#z6">Classroom 风险</a><a href="#z7">不要反复点读取</a></nav>
<section id="zh">
{zh(ed)}
</section>
<section id="en" class="lang-section" lang="en">
<p class="eyebrow">English</p>
<h1>Privacy Policy &amp; Risks</h1>
<p class="meta">{ed['app']} ({ed['en']}) · Last updated {UPDATED_EN}</p>
{en(ed)}
</section>
{editions_footer(slug)}
</main>
</body>
</html>
"""


def index():
    rows = [
        ["分发方式<br><small>Distribution</small>", "Xcode 自装<br>Personal install", "Xcode 自装<br>Personal install", "App Store", "TestFlight"],
        ["Jupiter", "自动同步 + 后台 + 保存登录<br>Auto, background, saved sign-in", "自动同步 + 后台 + 保存登录<br>Auto, background, saved sign-in", "手动读取；打开成绩页时更新<br>Manual; updates on open", "自动同步 + 后台 + 保存登录<br>Auto, background, saved sign-in"],
        ["Google Classroom", "网页登录 + Google 授权<br>Web sign-in + API", "网页登录 + Google 授权<br>Web sign-in + API", "仅 Google 授权<br>API only", "网页登录 + Google 授权<br>Web sign-in + API"],
        ["后台访问学校网站<br><small>Background school access</small>", "会 · Yes", "会 · Yes", "不会 · No", "会 · Yes"],
        ["复制保存登录 Cookie<br><small>Copies sign-in cookies</small>", "会 · Yes", "会 · Yes", "不会 · No", "会 · Yes"],
        ["风险等级<br><small>Risk</small>", "高 · Higher", "高 · Higher", "较低 · Lower", "高 · Higher"],
    ]
    head = ["", '<a href="original.html">原版</a>', '<a href="juntao.html">梁钧淘特别版</a>', '<a href="appstore.html">正式版</a>', '<a href="testflight.html">满血正式版</a>']
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Center 隐私政策</title>
<meta name="description" content="Student Center 各版本的隐私政策与风险说明">
<style>{CSS}</style>
</head>
<body>
<main>
<p class="eyebrow">Student Center</p>
<h1>隐私政策 · Privacy</h1>
<p class="meta">每个版本功能不同，隐私政策分开写。请打开你安装的那个版本。<br>Each edition works differently, so each has its own policy. Open the one you installed.<br>更新日期：{UPDATED_ZH}</p>
<div class="alert"><h3>不要反复点“读取成绩” · Don’t keep tapping “Read grades”</h3>
<p style="margin:0">每次读取都会打开 Jupiter 上你每一门课的页面。反复点按可能被当成机器人，导致限速或账号被临时锁定。<br>Each read opens every class page on Jupiter. Repeated taps can look like a bot and lead to rate limits or a temporary lock.</p></div>
{table(head, rows)}
<ul>
<li><a href="original.html">原版 · Original edition</a></li>
<li><a href="juntao.html">梁钧淘特别版 · Liang Juntao edition</a></li>
<li><a href="appstore.html">正式版（App Store）· App Store edition</a></li>
<li><a href="testflight.html">满血正式版（TestFlight）· Full edition (TestFlight)</a></li>
</ul>
<footer><p>Student Center 与 NYC DOE、Bayside High School、Jupiter、Clever、Google 均无关联。Not affiliated with NYC DOE, Bayside High School, Jupiter, Clever or Google.</p><p><a href="../">校历 · Calendar</a></p></footer>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent / "privacy"
    root.mkdir(exist_ok=True)
    for slug, ed in EDITIONS.items():
        (root / f"{slug}.html").write_text(page(slug, ed), encoding="utf-8")
    (root / "index.html").write_text(index(), encoding="utf-8")
    print("wrote", ", ".join(sorted(p.name for p in root.iterdir())))
