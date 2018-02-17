import pip

def install(package):
    pip.main(['install',package])

install('networkx')
install('geopy')
install('aiohttp')
install('python-socketio')



