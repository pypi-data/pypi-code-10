from IPython.core.display import display_html
from IPython import get_ipython

comm = None
listeners = {}

def setListener(topic, callback):
    listeners[topic] = callback

def dispatch(msg):
    # Note: because of the way comms are run, you can't print in these functions.
    # You can, however, hijack the comm_manager's logger, which prints to the kernel
    # stdout (wherever you have it running.)
    # e.g. get_ipython().kernel.comm_manager.log.error(...)
    msg = msg['content']['data']
    
    if listeners.has_key(msg['topic']):
        listeners[msg['topic']](msg['data'])

def handle_open(_comm, msg):
    global comm
    assert msg['content']['data'] == 'ipycomms.opened'
    comm = _comm
    _comm.on_msg(dispatch)

def send(topic, data):
    msg = {'topic': topic, 'data': data}
    comm.send(msg)

# The channel name is arbitrary.
get_ipython().kernel.comm_manager.register_target('ipycomms.channel', handle_open)

display_html('''
<script>

IPython.ipycomms = {
    init: function(){
        console.log("[ipycomms] initializing")
        this.comm = IPython.notebook.kernel.comm_manager.new_comm(
            'ipycomms.channel',
            "ipycomms.opened",  // Initial data sent with open (arbitrary)
            function(){},       // Callbacks
            "ipycomms.meta")    // Metadata (arbitrary)
        this.comm.on_msg(_.bind(this.dispatch, this))
    },
    dispatch: function(msg){
        msg = msg.content.data;
    
        if (!this.topicHandlers.hasOwnProperty(msg.topic)){
            console.log("[ipycomms] topic with no callback", msg.topic)
            return;
        }
        
        this.topicHandlers[msg.topic](msg.data)
    },
    topicHandlers: {},
    setListener: function(topic, callback){
        this.topicHandlers[topic] = callback
    },
    send: function(topic, data){
        this.comm.send({topic: topic, data: data})
    }
}

IPython.ipycomms.init()
</script>
''', raw=True)
print "Injected script."
