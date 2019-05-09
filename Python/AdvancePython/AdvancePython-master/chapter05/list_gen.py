#用简介的方式去遍历可迭代对象生成需要格式的列表
int_list = [1,2,3,4,5]

qu_list = [item * item for item in int_list]
print (type(qu_list))
int_list = [1,2,-3,4,5]

qu_list = [item if item > 0 else abs(item) for item in int_list]

#笛卡尔积
int_list1 = [1,2]
int_list2 = [3,4]

qu_list = [(first, second) for first in int_list1 for second in int_list2]

my_dict = {
    "key1":"bobby1",
    "key2":"bobby2"
}

# qu_list = [(key, value) for key, value in my_dict.items()]
#
# qu_list2 = list(((key, value) for key, value in my_dict.items()))
#
# for item in qu_list2:
#     print (item)

int_list = [1,2,3,4,5]

def process_item(item):
    return str(item)

int_dict = {process_item(item):item for item in int_list}
#列表生成式，第一：能用尽量用， 因为效率高
print (int_dict)


