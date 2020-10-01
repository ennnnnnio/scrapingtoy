from random_proxy import Random_Proxy

num = 0
while num < 200:
    proxy = Random_Proxy()
    # url = 'https://www.youtube.com/watch?v=gSl2ex-3Abc'
    url = 'https://valleyofuseless.blogspot.com/2020/09/my-second-post.html'
    request_type = "get"

    r = proxy.Proxy_Request(url=url, request_type=request_type)
    print(r)
