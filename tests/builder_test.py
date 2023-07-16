import logging
import os
import unittest

from mod_builder import builder

fixtures_folder = os.path.join(os.getcwd(), "fixtures")
log_string_format = '%(asctime)s  [%(levelname)s]: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_string_format)

DEFAULT_CONFIG = {
    "mod_folder": "/home/lidia/rtl8852be/",
    "mod_commands": ["make clean", "make -j8"],
    "mod_install_commands": ["sudo make install", "sudo modprobe 8852be"]
}

LOADED_CONFIG = {
    "mod_folder": "/home/bruno/git/rtl8852be/",
    "mod_commands": ["make clean", "make -j8"],
    "mod_install_commands": ["sudo make install", "sudo modprobe 8852be"]
}

LOADED_CONFIG_TEST_INSTALL = {
    "mod_folder": "/home/bruno/git/rtl8852be/",
    "mod_commands": ["make clean", "make -j8"],
    "mod_install_commands": ["sudo -S echo \"make install\"", "sudo -S echo \"modprobe 8852be\""]
}

class MyTestCase(unittest.TestCase):
    def test_can_read_config_when_not_there(self):
        config = builder.load_config(os.path.join(fixtures_folder, "not_existent.yaml"))
        self.assertIsNotNone(config)
        self.assertEqual(config, DEFAULT_CONFIG)

    def test_can_read_config_when_there(self):
        config = builder.load_config(os.path.join(fixtures_folder, "mod_builder_conf.yaml"))
        self.assertIsNotNone(config)
        self.assertEqual(config, LOADED_CONFIG)

    def test_can_execute_normal_build_actions(self):
        builds = builder.build(LOADED_CONFIG)
        self.assertTrue(builds)

    def test_can_install_module_in_best_case(self):
        installed = builder.install(LOADED_CONFIG_TEST_INSTALL)
        self.assertTrue(installed)


if __name__ == '__main__':
    unittest.main()
