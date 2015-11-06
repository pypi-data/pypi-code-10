"""

globalapis.py

string manipulation
dynamic loading

"""
globalapis_dict = {

    ######################
    # UNIX APIS
    ######################

    "unix" : {

        "memory" : {
            "malloc"        : "Memory Allocation",
            "calloc"        : "Allocate and initialize memory",
        },

        "scheduler" : {
            "fork"           : "Fork Child Process",
            "pthread_create" : "Spawn thread",
        },
    },

    ######################
    # LINUX KERNEL APIS
    ######################

    "linuxkernel" : {

        "memory" : {

        },

        "scheduler" : {

        },
    },


    ######################
    # BCM APIS
    ######################

    "bcm" : {
        "memory" : {

        },

        "scheduler" : {

        },
    },
}

