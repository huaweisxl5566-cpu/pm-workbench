# PM Workbench 部署指南

## 前置准备

1. 注册 [GitHub](https://github.com) 账号
2. 注册 [Vercel](https://vercel.com) 账号（用 GitHub 登录）
3. 注册 [Railway](https://railway.app) 账号（用 GitHub 登录）
4. 安装 [Git](https://git-scm.com)

## 第一步：创建 GitHub 仓库

```bash
cd F:\files\AI\pm-workbench

# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 在 GitHub 上创建新仓库 pm-workbench，然后：
git remote add origin https://github.com/你的用户名/pm-workbench.git
git branch -M main
git push -u origin main
```

## 第二步：部署后端到 Railway

1. 登录 [railway.app](https://railway.app)
2. 点击 **New Project** → **Deploy from GitHub Repo**
3. 选择你的 `pm-workbench` 仓库
4. **Settings** → **Service Settings**：
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 部署完成后，点击 **Settings** → **Networking** → **Generate Domain**
6. 记下生成的域名，例如：`pm-workbench-production.up.railway.app`

## 第三步：更新前端 API 地址

打开 `frontend/vercel.json`，将 `your-app.up.railway.app` 替换为你的 Railway 域名：

```json
{
  "rewrites": [
    { 
      "source": "/api/(.*)", 
      "destination": "https://pm-workbench-production.up.railway.app/api/$1" 
    }
  ]
}
```

然后推送到 GitHub：
```bash
git add .
git commit -m "Update API URL for production"
git push
```

## 第四步：部署前端到 Vercel

1. 登录 [vercel.com](https://vercel.com)
2. 点击 **Add New...** → **Project**
3. 选择你的 `pm-workbench` 仓库
4. 配置：
   - Framework Preset: **Vue**
   - Root Directory: **frontend**
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. 点击 **Deploy**

部署完成后，你会获得一个 `xxx.vercel.app` 域名。

## 第五步：绑定自定义域名（可选）

### Vercel
1. 在 Vercel 项目 Settings → Domains
2. 输入你的域名，按提示配置 DNS

### Railway
1. 在 Railway 项目 Settings → Domains
2. 输入你的域名，按提示配置 DNS

## 常见问题

### 后端 CORS 错误
如果遇到 CORS 错误，检查 `backend/main.py` 中的 `allow_origins` 配置。

### 数据库问题
Railway 使用 SQLite 时数据会在重启后丢失。如需持久化，建议：
1. 使用 Railway 的 PostgreSQL 插件
2. 或使用外部数据库服务

### 环境变量
在 Railway 控制台的 Variables 标签页可以设置环境变量。

## 费用估算

- **Vercel**: 免费额度足够个人使用
- **Railway**: 每月 $5 免费额度，轻量应用足够
- **总费用**: 约 0-5 美元/月
