from conans import ConanFile
from conans import tools
from conans.tools import download, unzip, check_md5, os_info, pythonpath, environment_append

import os
from os import path

class GmpConan(ConanFile):
    name = "gmp"
    version = "6.1.2"
    url = "http://github.com/DEGoodmanWilson/conan-gmp"
    ZIP_FOLDER_NAME = "gmp-%s" % version
    settings =  "os", "compiler", "arch"
    license = "LGPLv3 or GPLv2"
    options = {
        "shared": [True, False],
        "disable_assembly": [True, False],
        "enable_fat": [True, False],
        "enable_cxx": [True, False],
        "disable-fft": [True, False],
        "enable-assert": [True, False]
    }
    default_options = (
        "shared=False",
        "disable_assembly=False",
        "enable_fat=False",
        "enable_cxx=True",
        "disable-fft=False",
        "enable-assert=False"
    )

    requires = (
        "AutotoolsHelper/0.0.2@noface/experimental"
    )

    SHA256 = "5275bb04f4863a13516b2f39392ac5e272f5e1bb8057b18aec1c9b79d73d8fb2"

    def source(self):
        zip_name = "gmp-%s.tar.bz2" % self.version
        download("http://gmplib.org/download/gmp/%s" % zip_name, zip_name)
        tools.check_sha256(zip_name, self.SHA256)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        self.prepare_build()
        self.configure_and_make()

    def package(self):
        SRC = self.ZIP_FOLDER_NAME

        self.copy("*.h", "include", src=SRC, keep_path=True)
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=SRC, keep_path=False)
            self.copy(pattern="*.dll*", dst="bin", src=SRC, keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src=SRC, keep_path=False)

        self.copy(pattern="*.lib", dst="lib", src=SRC, keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = ['gmp']


    ##################################################################################################

    def prepare_build(self):
        if getattr(self, "package_folder", None) is None:
            self.package_folder = path.abspath(path.join(".", "install"))
            self._try_make_dir(self.package_folder)

    def configure_and_make(self):
        extra_env = {}

        if self.settings.arch == "x86":
            extra_env["ABI"]="32"

        with tools.chdir(self.ZIP_FOLDER_NAME), pythonpath(self), environment_append(extra_env):
            from autotools_helper import Autotools

            autot = Autotools(self,
               shared      = self.options.shared)

            self.autotools_build(autot)

    def autotools_build(self, autot):
        self.add_options(autot)

        if os_info.is_macos:
            autot.with_feature("pic")

        self.output.info("options = " + str(autot.options))

        autot.configure()
        autot.build()
        autot.install()

    def add_options(self, autot):
        for option_name in self.options.values.fields:
            if not getattr(self.options, option_name) or option_name == "shared":
                continue

            self.output.info("Activate option: %s" % option_name)

            opt = option_name.replace("_", "-").split("-")

            if opt[0] == "enable":
                autot.enable(opt[1])
            elif opt[0] == "disable":
                autot.enable(opt[1])

    def _try_make_dir(self, folder):
        try:
            os.mkdir(folder)
        except OSError:
            #dir already exist
            pass
