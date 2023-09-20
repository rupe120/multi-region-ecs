# examples/server_simple.py
from aiohttp import web

async def handle(request):
    if request.headers.get('user-agent') == 'ELB-HealthChecker/2.0':
        return web.Response(status=200)
    
    print('------------------')
    print('Received request:')
    print(request)
    
    return_value = web.Response(
        status=200
    )
    print('returning response:')
    print(return_value)
    return return_value


app = web.Application()
app.add_routes([web.route('*','/', handle)])

def main(args):
    return app