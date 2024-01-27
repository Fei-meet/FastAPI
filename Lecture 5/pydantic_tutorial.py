from pydantic import BaseModel, ValidationError, constr
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional
from sqlalchemy import Column,Integer,String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

print("\033[31m1. --- Pydetic 的基本用法。Pycharm 可以安装Pydantic插件 ---\033[0m")
class User (BaseModel):
    id: int # 必填字段
    name: str = "John Snow" # 选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = [] # 列表中元素是int或者可以直接转换成int

extrnal_data = {
    "id": "123",
    "signup_ts": "2022-12-22 12:22",
    "friends": [1,2,"3"] # 3 是可int（“3”）的
}

user = User(**extrnal_data)
print(user.id, user.friends)
print(repr(user.signup_ts))
print(user.dict())

print("\033[31m2. --- 校验失败处理 ---\033[0m")
try:
    User(id=1,signup_ts= datetime.today(),friends=[1,2,"not number"])
except ValidationError as e:
    print(e.json())

print("\033[31m3. --- 模型类的属性和方法 ---\033[0m")
print(user.dict())
print(user.json())
print(user.copy())
print(User.parse_obj(obj = extrnal_data))
print(User.parse_raw('{"id": "123","signup_ts": "2022-12-22 12:22","friends": [1,2,"3"]}'))

path = Path('pydantic_tutorial.json')
path.write_text('{"id": "123","signup_ts": "2022-12-22 12:22","friends": [1,2,"3"]}')
print(User.parse_file(path))

print(user.schema())
print(user.schema_json())

# construct不校验数据，直接创建
user_data = {"id": "error","signup_ts": "2022-12-22 12:22","friends": [1,2,"3"]} # id 是字符串，不符合
print(User.construct(**user_data))

print((User.__fields__.keys())) # 定义模型类的时候，所有字段都注明类型，字段顺序就不会乱

print("\033[31m4. --- 递归模型 ---\033[0m")

class Sound(BaseModel):
    sound: str

class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]

dogs = Dog(birthday = date.today(), weight = 6.66, sound = [{"sound":"wang wang~"},{"sound":"ying ying~"}])

print(dogs.dict())

print("\033[31m5. --- ORM模型类：从类实例创建符合ORM对象的模型 ---\033[0m")
Base = declarative_base()

class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer,primary_key = True, nullable = False)
    public_key = Column(String(20), index = True, nullable = False, unique = True)
    name = Column(String(63),unique = True)
    domains = Column(ARRAY(String(255)))

class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length = 20)
    name: constr(max_length = 63)
    domains: List[constr(max_length = 255)]

    class Config:
        orm_mode = True

co_orm = CompanyOrm(
    id = 123,
    public_key='foobar',
    name = 'Testing',
    domains= ['example.com', 'imooc.com']
)

print(CompanyMode.from_orm(co_orm))
