from conans import ConanFile
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake
import patch

class Proj4Conan(ConanFile):
    name = "Proj4"
    version = "4.9.3"
    settings = "os", "compiler", "build_type", "arch"
    folder = "proj.4-%s" % version
    generators = "cmake"
    url = "https://github.com/OSGeo/proj.4"
    zip_name = "%s.tar.gz" % version
    download_url = "https://github.com/OSGeo/proj.4/archive/%s" % zip_name
    license = "LGPL"
    exports = "proj4-%s.patch" % version

    def source(self):
        download(self.download_url, self.zip_name)
        unzip(self.zip_name)
        os.unlink(self.zip_name)
        pset = patch.fromfile("proj4-%s.patch" % self.version)
        pset.apply()
			
    def build(self):
        cmake = CMake(self)
        os.makedirs('build')
        config = "-DPROJ4_TESTS=OFF -DBUILD_LIBPROJ_SHARED=ON"
        #-DBUILD_CS2CS=OFF -DBUILD_PROJ=OFF -DBUILD_GEOD=OFF -DBUILD_NAD2BIN=OFF"
        self.run('cmake ../%s %s %s' % (self.folder, config, cmake.command_line), cwd='build')
        self.run('cmake --build build ' + cmake.build_config)

    def package(self):
        """ Define your conan structure: headers, libs and data. After building your
            project, this method is called to create a defined structure:
        """
        self.copy(pattern="*.h", dst="include", src="%s/src" % self.folder, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="lib", keep_path=False)        
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            libname = "proj4"    # ?
        else:
            libname = "proj4"
        self.cpp_info.libs = [libname]
