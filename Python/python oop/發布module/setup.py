from distutils.core import setup

setup(name = "hm_message",
      version = "1.0",
      description = "itheima's 發送和接收消息模組",
      long_description="完整的發送和接收消息模組",
      author='shocklee',
      author_email="ronan1008@yahoo.com.tw",
      url="www.shocklee.com",
      py_modules=["hm_message.send_message",
                  "hm_message.receive_message"])

