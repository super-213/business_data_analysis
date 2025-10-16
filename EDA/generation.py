from faker import Faker
import pandas as pd
import random

fake = Faker('zh_CN')  # 使用中文环境

# ------------------------------
# 1️⃣ 生成用户表 user_unique_compare
# ------------------------------
users = []
for i in range(1000):
    user_id = f"U{20251000000 + i}"
    users.append({
        "user_id": user_id,
        "nickname": fake.first_name(),
        "platform": random.choice(["淘宝", "抖音", "微信"]),
        "gender": random.choice(["male", "female"]),
        "region": fake.province()
    })
df_users = pd.DataFrame(users)
df_users.to_csv("user_unique_compare.csv", index=False, encoding="utf-8-sig")

# ------------------------------
# 2️⃣ 生成 SPU 表 spu_manages_feishu
# ------------------------------
spus = []
for i in range(200):
    spu_id = f"SPU{i:03d}"
    title = random.choice([
        "针织连衣裙", "牛仔裤", "休闲衬衫", "羽绒服", "西装外套",
        "半身裙", "运动鞋", "高跟鞋", "T恤", "卫衣"
    ]) + random.choice(["春季款", "夏季款", "秋冬款", "经典款"])
    cost = round(random.uniform(50, 400), 2)
    profit_margin = round(random.uniform(0.2, 0.6), 2)
    spus.append({
        "spu": spu_id,
        "title": title,
        "cost": cost,
        "inventory": random.randint(100, 1000),
        "profit_margin": profit_margin
    })
df_spus = pd.DataFrame(spus)
df_spus.to_csv("spu_manages_feishu.csv", index=False, encoding="utf-8-sig")

# ------------------------------
# 3️⃣ 生成 SKU 表 sku_data_base
# 每个 SPU 对应 3–5 个 SKU
# ------------------------------
colors = ["红色", "黑色", "白色", "蓝色", "灰色", "粉色", "米色"]
sizes = ["XS", "S", "M", "L", "XL"]
categories = ["女装", "男装", "鞋靴", "配饰"]

skus = []
for spu in spus:
    for _ in range(random.randint(3, 5)):
        sku_id = f"SKU{random.randint(10000, 99999)}"
        skus.append({
            "sku": sku_id,
            "spu": spu["spu"],
            "name": spu["title"],
            "category": random.choice(categories),
            "color": random.choice(colors),
            "size": random.choice(sizes),
            "price": round(spu["cost"] * (1 + spu["profit_margin"] + random.uniform(0.05, 0.15)), 2)
        })
df_skus = pd.DataFrame(skus)
df_skus.to_csv("sku_data_base.csv", index=False, encoding="utf-8-sig")

# ------------------------------
# 4️⃣ 生成 SKU 销售统计表 new_sku_sales
# ------------------------------
sku_sales = []
for sku in df_skus["sku"]:
    sales = random.randint(50, 2000)
    sku_sales.append({
        "sku": sku,
        "sales": sales,
        "add_to_cart": random.randint(int(sales * 0.8), sales * 2),
        "favorite": random.randint(10, 300),
        "refund_rate": round(random.uniform(0.01, 0.15), 2)
    })
df_sales = pd.DataFrame(sku_sales)
df_sales.to_csv("new_sku_sales.csv", index=False, encoding="utf-8-sig")

# ------------------------------
# 5️⃣ 生成订单表 erp_order
# 从用户表与 SKU 表中随机抽取
# ------------------------------
orders = []
for i in range(2000):
    user = random.choice(users)
    sku = random.choice(skus)
    quantity = random.randint(1, 5)
    order_price = sku["price"]
    total = round(order_price * quantity, 2)
    orders.append({
        "order_id": f"O{20251000000 + i}",
        "user_id": user["user_id"],
        "sku": sku["sku"],
        "quantity": quantity,
        "price": order_price,
        "total_amount": total,
        "order_date": fake.date_between(start_date='-90d', end_date='today'),
        "status": random.choice(["paid", "shipped", "refunded"])
    })
df_orders = pd.DataFrame(orders)
df_orders.to_csv("erp_order.csv", index=False, encoding="utf-8-sig")

print("✅ 数据生成完毕，共生成 5 个 CSV 文件：")
print("- user_unique_compare.csv")
print("- spu_manages_feishu.csv")
print("- sku_data_base.csv")
print("- new_sku_sales.csv")
print("- erp_order.csv")