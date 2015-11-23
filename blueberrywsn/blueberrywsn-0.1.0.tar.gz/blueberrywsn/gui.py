import Tkinter as Tk
import operator

from pi import Pi


class ServerGui(Tk.Tk, object):
    def __init__(self):
        super(ServerGui, self).__init__()

        self.title('Distributed Systems - 802.15.1')

        frame_main = Tk.Frame(self)
        frame_main.grid(sticky='nswe', padx=15, pady=15)

        frame_list = Tk.LabelFrame(frame_main, text='Rede Bluetooth')
        frame_list.grid(sticky='we')
        self.list = Tk.Listbox(frame_list, height=39, width=70)
        self.list.grid(row=0, column=0, sticky='we')
        scrollbar_list = Tk.Scrollbar(frame_list, command=self.list.yview)
        scrollbar_list.grid(row=0, column=1, sticky='nsew')
        self.list['yscrollcommand'] = scrollbar_list.set

        self.pi = Pi()
        self.pi.start()

        self.after(1000, self.keep_updating)

    def update_list(self):
        counter = sorted(self.pi.devices.items(), key=operator.itemgetter(0))
        self.list.delete(0, Tk.END)
        if counter:
            for device, level in counter:
                self.list.insert(Tk.END, device + ' ' + str(level))
        else:
            self.list.insert(Tk.END, 'There are no active devices')

    def keep_updating(self):
        self.update_list()
        self.after(1000, self.keep_updating)


def main():
    ServerGui().mainloop()


if __name__ == '__main__':
    main()
