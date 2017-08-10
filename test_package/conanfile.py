from conans.model.conan_file import ConanFile
from conans import CMake
import os


############### CONFIGURE THESE VALUES ##################
default_user = "DEGoodmanWilson"
default_channel = "testing"
#########################################################

version_lib  = "6.1.2"
channel  = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "gmp/%s@%s/%s" % (version_lib, username, channel)

    build_requires = "cmake_installer/0.1@lasote/stable"

    def build(self):
        self.build_dir = os.path.abspath(".")

        cmake = CMake(self)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run('cmake --build . %s' % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        
    def test(self):
        self.run('"%s" 10' % os.path.join(self.build_dir, "bin", "example"))
