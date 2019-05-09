import numbers


class BaseField:
    def __init__(self, db_column=""):
        self.column = db_column


class IntField(BaseField):
    def __init__(self, max_value=None, min_value=None):
        self.max_value = max_value
        self.min_value = min_value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError('Must be Inter')
        if value < 0:
            raise ValueError('Negative value not allowed')
        if self.min_value is not None:
            if value < self.min_value:
                raise ValueError('min_value is not satified')
        if self.max_value is not None:
            if value > self.max_value:
                raise ValueError('max_value is not satified')
        instance.__dict__[self.name] = value


class CharField(BaseField):
    def __init__(self, max_length=None):
        if max_length is None:
            raise ValueError('max_length is required')
        if max_length<=0:
            raise ValueError('max_length must be positive')
        self.max_length = max_length

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError('Must be Inter')
        if value < 0:
            raise ValueError('Negative value not allowed')
        if self.min_value is not None:
            if value < self.min_value:
                raise ValueError('min_value is not satified')
        if self.max_value is not None:
            if value > self.max_value:
                raise ValueError('max_value is not satified')
        instance.__dict__[self.name] = value


class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

#二、定义元类，控制Model对象的创建
class ModelMetaclass(type):
    '''定义元类'''
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return super(ModelMetaclass,cls).__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.items():
            # 保存类属性和列的映射关系到mappings字典
            if isinstance(v, Field):
                print('Found mapping: %s==>%s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            #将类属性移除，使定义的类字段不污染User类属性，只在实例中可以访问这些key
            attrs.pop(k)
        attrs['__table__'] = name.lower() # 假设表名和为类名的小写,创建类时添加一个__table__类属性
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系，创建类时添加一个__mappings__类属性
        return super(ModelMetaclass,cls).__new__(cls, name, bases, attrs)

#三、编写Model基类
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

    class Meta:
        db_table = "users"

#最后，我们使用定义好的ORM接口，使用起来非常的简单。
class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

# 创建一个实例：
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
# 保存到数据库：
u.save()

#输出
# Found mapping: email==><StringField:email>
# Found mapping: password==><StringField:password>
# Found mapping: id==><IntegerField:id>
# Found mapping: name==><StringField:username>
# SQL: insert into User (password,email,username,id) values (?,?,?,?)
# ARGS: ['my-pwd', 'test@orm.org', 'Michael', 12345]
