import os
import types
import unittest
import tempfile
from pluginmanager.plugin_interface import PluginInterface
from pluginmanager.iplugin import IPlugin


class TestInterface(unittest.TestCase):
    def setUp(self):
        self.test_obj = IPlugin()
        self.interface = PluginInterface()

        # fixes weird state issues on my machine
        self.interface.file_manager.set_file_filters([])
        self.interface.module_manager.set_module_filters([])

    def test_collect_plugin_directories(self):
        dir_names = []
        dirs = []
        with tempfile.TemporaryDirectory() as main_dir:
            self.interface.set_plugin_directories(main_dir)
            dir_names.append(main_dir)
            with tempfile.TemporaryDirectory(dir=main_dir) as recursive_dir:
                dir_names.append(recursive_dir)
                dirs = self.interface.collect_plugin_directories(main_dir)
        self.assertIn(dir_names[0], dirs)
        self.assertIn(dir_names[1], dirs)

    def test_collect_plugin_filepaths(self):
        filename = 'test.py'
        filepaths = []
        with tempfile.TemporaryDirectory() as main_dir:
            filename = os.path.join(main_dir, filename)
            open(filename, 'a+').close()
            filepaths = self.interface.collect_plugin_filepaths(main_dir)
        self.assertIn(filename, filepaths)

    def test_load_modules(self):
        module = None
        with tempfile.NamedTemporaryFile(suffix='.py') as file:
            file.write(b'test=1')
            file.seek(0)
            module = self.interface.load_modules(file.name)
        module = module.pop()
        self.assertEqual(module.test, 1)

    def test_collect_plugins(self):
        module = types.ModuleType('test')
        module.test = 5
        plugins = self.interface.collect_plugins(module)
        self.assertIn(5, plugins)

    def test_track_site_package_path(self):
        # TODO: better test method
        num_directories = len(self.interface.get_plugin_directories())
        self.interface.track_site_package_paths()
        new_num_dirs = len(self.interface.get_plugin_directories())
        self.assertTrue(new_num_dirs > num_directories)

    def test_adders_getters_and_setters(self):
        adders = ['add_plugin_filepaths',
                  'add_plugins']

        getters = ['get_plugin_filepaths',
                   'get_plugins']

        setters = ['set_plugin_filepaths',
                   'set_plugins']

        all_ = [adders, getters, setters]
        for index, value in enumerate(all_):
            all_[index] = [getattr(self.interface, name) for name in value]
        adders, getters, setters = all_
        test_obj = IPlugin()
        for index, (adder, getter, setter) in enumerate(zip(adders,
                                                            getters,
                                                            setters)):
            adder(self.test_obj)
            self.assertIn(self.test_obj,
                          getter(),
                          '{} not found in {} from {}'.format(self.test_obj,
                                                              getter(),
                                                              adder))

            setter(test_obj)
            self.assertIn(test_obj, getter())
            self.assertNotIn(self.test_obj, getter())

    def test_set_plugins(self):
        self.interface.set_plugins(self.test_obj)
        plugins = self.interface.get_plugins()
        self.assertIn(self.test_obj, plugins)
