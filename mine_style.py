
def style(style_name, **kwargs):
    return _style_loader.style(style_name, **kwargs)

class MineStyle(object):

    @staticmethod
    def swept(num):
        colors = ['#BBBBBB',

                  '#000000',

                  '#0602E7',

                  '#F52703',

                  '#6F3F17',

                  '#FFFE07',

                  '#FF12FF',

                  '#3EE8D3',

                  '#FDFCD6'

                  ]
        return {'relief': 'sunken', 'text': num or ' ', 'bg': '#DDDDDD', 'fg': colors[num]}

    unknown = {'relief': 'raised', 'text': '', 'bg': '#DDDDDD', 'fg': '#000000'}

    marked = {'relief': 'raised', 'text': '?', 'bg': '#DDDDDD', 'fg': '#000000'}

    mine = {'relief': 'sunken', 'text': 'X', 'bg': '#D71A23', 'fg': '#FFFFFF'}

class StyleLoader(object):

    def style(self, style_name, **kwargs):
        func = reduce(getattr, style_name.split('.'), self)
        return func(**kwargs) if callable(func) else func

    def register(self, style_pre, obj):
        setattr(self, style_pre, obj)

_style_loader = StyleLoader()
_style_loader.register('grid',MineStyle)
style('grid.marked')




