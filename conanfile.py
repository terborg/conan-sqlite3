#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ConanSqlite3(ConanFile):
    name = "sqlite3"
    version = "3.21.0"
    year = "2017"
    sha1 = "ebe33c20d37a715db95288010c1009cd560f2452"
    license = "https://sqlite.org/copyright.html"
    settings = "os", "compiler", "arch", "build_type"
    url = "http://github.com/bincrafters/conan-sqlite3"
    exports = ["CMakeLists.txt", "FindSQLite3.cmake"]
    description = "Self-contained, serverless, in-process SQL database engine."
    
    def source(self):
        base_url = "https://www.sqlite.org/" + self.year
        archive_name = "sqlite-amalgamation-" + self.version.replace(".","") + "000"
        archive_ext = "zip"
        download_url = "{0}/{1}.{2}".format(base_url, archive_name, archive_ext)
        self.output.info("Attempting download of sources from: " + download_url)
        tools.get(download_url, sha1=self.sha1)
        
        os.rename(archive_name, "sources")
        os.rename("CMakeLists.txt", os.path.join("sources", "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        self.copy("FindSQLite3.cmake", ".", ".")
        self.copy("*.h", dst="include", src="sources")
        self.copy(pattern="*.lib", dst="lib", src="Release", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="sources", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.pdb", dst="lib", src="sources", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['sqlite3']
        if not self.settings.os == "Windows":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("dl")
