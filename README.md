# UrbanVista Web Demo
## Mô tả
UrbanVista là một ứng dụng web giúp quản lý và trực quan hóa dữ liệu đô thị. Phần demo này hướng dẫn cách chạy ứng dụng trên localhost.

## Yêu cầu cài đặt
* Node.js v16 trở lên
* npm (Node Package Manager)

## Cách chạy demo web
1. Clone repo về máy
2. Truy cập vào folder fe
3. Tạo 1 file .env với nội dung như sau:
   ```
   DATABASE_URL=postgresql://urbanvista_owner:npg_MRsUt0LGrPp9@ep-yellow-wave-a8g4ezr7-pooler.eastus2.azure.neon.tech/urbanvista?sslmode=require
   BETTER_AUTH_SECRET=3YsKND1GK9mfg11w6m8vqqqteDpfrpA6
   BETTER_AUTH_URL=http://localhost:3000
   ```
5. Khởi tại 1 terminal mới và chạy các lệnh sau theo thứ tự:
   - `npm install`
   - `npm run build`
   - `npm run start`
  
6. Truy cập vào [`đường dẫn`](http://localhost:3000/)

## Backend API
A simple FastAPI service is provided in `backend/` to read polygon and building data from a PostgreSQL database. The ORM models mirror the schema described in the documentation (Building, Floor, BodyComp, etc.).

### Setup
1. Install requirements (FastAPI and SQLAlchemy).
2. Set `DATABASE_URL` environment variable to your PostgreSQL connection string.
3. Run the service:
   ```bash
   uvicorn backend.app:app --reload
   ```

### Loading data
To import polygons from a JSON file, call the helper:
```python
from backend.app import load_from_json, SessionLocal
with SessionLocal() as session:
    load_from_json("path/to/polygons.json", session)
```
