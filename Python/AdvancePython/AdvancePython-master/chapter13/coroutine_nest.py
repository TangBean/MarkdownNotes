#1. run_until_complete
# import asyncio
# loop = asyncio.get_event_loop()
# loop.run_forever()
# loop.run_until_complete()

#1. loop会被放到future中
#2. 取消future(task)

# import asyncio
# import time
#
# async def get_html(sleep_times):
#     print("waiting")
#     await asyncio.sleep(sleep_times)
#     print("done after {}s".format(sleep_times))
#
#
# if __name__ == "__main__":
#     task1 = get_html(2)
#     task2 = get_html(3)
#     task3 = get_html(3)
#
#     tasks = [task1, task2, task3]
#
#     loop = asyncio.get_event_loop()
#
#     try:
#         loop.run_until_complete(asyncio.wait(tasks))
#     except KeyboardInterrupt as e:
#         all_tasks = asyncio.Task.all_tasks()
#         for task in all_tasks:
#             print("cancel task")
#             print(task.cancel())
#         loop.stop()
#         loop.run_forever()
#     finally:
#         loop.close()

#注册协程到loop中有两种方法
#1. 通过ensure_future/create_task
#2. await
