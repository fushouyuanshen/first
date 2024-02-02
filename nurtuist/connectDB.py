import pymysql


def get_conn():
    # 获取MYSQL的链接
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='040722',
        database='test',
        charset='utf8'
    )


def query_data(sql):
    # 查询信息，已弃用
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def select_date(data):
    # 查找姓名、密码对应的用户
    conn = get_conn()
    sql = """
    SELECT username, password FROM nurtuist
    WHERE username = %s
    AND password = %s
    """
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        result = cursor.fetchone()
        return result
    finally:
        conn.close()


def insert_name(data):
    # 注册
    sql = """
        INSERT INTO 
        nurtuist(username,password) 
        VALUES(%s, %s);
    """
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        conn.commit()
    finally:
        conn.close()


def update(data):
    # 更新已存在用户的数据
    sql = """
        UPDATE nurtuist SET sex=%s, age=%s, weight=%s, height=%s, body_fat_rate=%s, blood_sugar=%s, food_preference=%s,
        diet_plan_Monday=%s, diet_plan_Tuesday=%s, diet_plan_Wednesday=%s, diet_plan_Thursday=%s, 
        diet_plan_Friday=%s, diet_plan_Saturday=%s, diet_plan_Sunday=%s
        WHERE username=%s;
    """
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        conn.commit()
    finally:
        conn.close()


def select_food(data):
    # 查找对应用户的食谱
    conn = get_conn()
    sql = """
        SELECT diet_plan_Monday, diet_plan_Tuesday, diet_plan_Wednesday, diet_plan_Thursday,
        diet_plan_Friday, diet_plan_Saturday, diet_plan_Sunday FROM nurtuist WHERE username = %s
        """
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        result = cursor.fetchone()
        return result
    finally:
        conn.close()


def create_db(table_name):
    # 创建数据库，初始化数据库时使用
    table_schema = """
        CREATE TABLE IF NOT EXISTS nurtuist (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL,  -- 建议使用hash后的密码存储，并且考虑加盐
            sex VARCHAR(10),
            age INT,
            height DECIMAL(5,2),   -- 身高可以是小数，所以用DECIMAL类型
            weight DECIMAL(6,2),   -- 体重也可以是小数
            body_fat_rate DECIMAL(6, 2),  -- 体脂率通常也是小数
            blood_sugar DECIMAL(6, 2),  -- 血糖值可能也需要支持小数
            food_preference TEXT,  -- 食物偏好可以是文本描述，如果需要更结构化的数据，可考虑其他方式如JSON或关联其他表
            diet_plan_Monday TEXT,  -- 食谱同理，可以用TEXT类型存储，复杂情况下也可以关联其他表
            diet_plan_Tuesday TEXT,
            diet_plan_Wednesday TEXT,
            diet_plan_Thursday TEXT,
            diet_plan_Friday TEXT,
            diet_plan_Saturday TEXT,
            diet_plan_Sunday TEXT
        )
        """
    # 创建数据库
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        check_sql = f"SHOW TABLES LIKE '{table_name}'"
        cursor.execute(check_sql)
        if cursor.fetchone() is None:
            cursor.execute(table_schema)
        conn.commit()
    finally:
        conn.close()


def main():
    table_name = "nurtuist"
    create_db(table_name)


if __name__ == '__main__':
    main()
