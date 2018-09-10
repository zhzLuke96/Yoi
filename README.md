# Yoi
Asynchronous HTTP server framework for asyncio(come soon) and Python

# todo
- [x] router.wrapper
- [x] router.static_folder
- [x] globals.cookies
- [x] globals.session
- [x] globals.server_session (ip_agent)
- [ ] mimetype_waring
- [ ] more_method: post put del...
- [ ] more_Type: json
- [ ] cache_setting
- [ ] cache_response
- [ ] asyncio

> log 18/9/10:
> <br>问题还很多，本来准备直接写异步的东西...看了下wsgi对异步支持非常差，需要套一层同步异步切换引擎？大概是这个节奏，看上去还很远
> <br>有点不懂的就是flask中，既然同一个线程只有一个stack，那么还有必要用stack吗？直接一个全局指针不就行了，实在有点不理解怎么会存在两个request处于同一个栈中的情况...(当然，协程的话stack是很必要的)


# asyncio
come soon..

# 后
想融合flask和aiohttp于是写了这个东西(其实是练手作...)
