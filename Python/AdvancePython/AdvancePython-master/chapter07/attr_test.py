# coding=utf-8
class DataDescriptor(object):
    def __init__(self, init_value):
        self.value = init_value

    def __get__(self, instance, typ):
        return 'DataDescriptor __get__'

    def __set__(self, instance, value):
        print('DataDescriptor __set__')
        self.value = value


class NonDataDescriptor(object):
    def __init__(self, init_value):
        self.value = init_value

    def __get__(self, instance, typ):
        return ('NonDataDescriptor __get__')


class Base(object):
    dd_base = DataDescriptor(0)
    ndd_base = NonDataDescriptor(0)


class Derive(Base):
    dd_derive = DataDescriptor(0)
    ndd_derive = NonDataDescriptor(0)
    same_name_attr = 'attr in class'

    def __init__(self):
        self.not_des_attr = 'I am not descriptor attr'
        self.same_name_attr = 'attr in object'

    def __getattr__(self, key):
        return '__getattr__ with key %s' % key

    def change_attr(self):
        self.__dict__['dd_base'] = 'dd_base now in object dict '
        self.__dict__['ndd_derive'] = 'ndd_derive now in object dict '


def main():
    b = Base()
    d = Derive()
    print ('Derive object dict', d.__dict__)
    assert d.dd_base == "DataDescriptor __get__"
    assert d.ndd_derive == 'NonDataDescriptor __get__'
    assert d.not_des_attr == 'I am not descriptor attr'
    assert d.no_exists_key == '__getattr__ with key no_exists_key'
    assert d.same_name_attr == 'attr in object'
    d.change_attr()
    print  ('Derive object dict', d.__dict__)
    assert d.dd_base != 'dd_base now in object dict '
    assert d.ndd_derive == 'ndd_derive now in object dict '

    try:
        b.no_exists_key
    except Exception as e:
        assert isinstance(e, AttributeError)


if __name__ == '__main__':
    main()
