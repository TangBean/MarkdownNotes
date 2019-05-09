a = {"bobby1":{"company":"imooc"},
     "bobby2": {"company": "imooc2"}
     }
#clear
# a.clear()
# pass

#copy, 返回浅拷贝
new_dict = a.copy()
new_dict["bobby1"]["company"] = "imooc3"

#formkeys
new_list = ["bobby1", "bobby2"]

new_dict = dict.fromkeys(new_list, {"company":"imooc"})

new_dict.update((("bobby","imooc"),))

