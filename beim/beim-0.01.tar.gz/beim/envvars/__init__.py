# environment variables

def perform(operations):
    from renderers.Performer import Performer
    p = Performer()
    return p.render(operations)
