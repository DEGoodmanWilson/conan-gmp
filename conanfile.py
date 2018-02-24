#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class GmpConan(ConanFile):
    name = "gmp"
    version = "6.1.1"
    url = "http://github.com/DEGoodmanWilson/conan-gmp"
    description = "The GNU bignum library"
    license = "https://gmplib.org/manual/Copying.html#Copying"
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "disable-assembly": [True, False],
               "enable-fat": [True, False],
               "enable-cxx": [True, False],
               "disable-fft": [True, False],
               "enable-assert": [True, False]}
    default_options = "shared=False", "disable-assembly=False", "enable-fat=False", \
                      "enable-cxx=True", "disable-fft=False", "enable-assert=False"

    def source(self):
        source_url = "http://gnu.uberglobalmirror.com/gmp"
        tools.get("{0}/gmp-{1}.tar.bz2".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        with tools.chdir("sources"):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True

            config_args = []
            for option_name in self.options.values.fields:
                if(option_name == "shared"):
                    if(getattr(self.options, "shared")):
                        config_args.append("--enable-shared")
                    else:
                        config_args.append("--enable-static")
                else:
                    activated = getattr(self.options, option_name)
                    if activated:
                        self.output.info("Activated option! %s" % option_name)
                        config_args.append("--%s" % option_name)


            env_build.configure(args=config_args)
            env_build.make()
       
    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
            self.copy(pattern="*", dst="include", src="include")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)


