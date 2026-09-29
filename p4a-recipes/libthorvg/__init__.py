from os.path import join
from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory, shprint
import sh


class LibthorvgRecipe(Recipe):
    version = '0.13.5'
    url = 'https://github.com/thorvg/thorvg/archive/refs/tags/v{version}.tar.gz'
    patches = []
    depends = []

    def should_build(self, arch):
        return True

    def get_include_dirs(self, arch):
        return [join(self.get_build_dir(arch.arch), 'install', 'include', 'thorvg-1')]

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            # Указываем meson source и build dir явно
            shprint(
                sh.Command('meson'),
                'setup',
                'builddir',                     # куда собирать
                '.',                            # откуда брать исходники (текущая папка)
                '--cross-file', 'tmp/android.meson.cross',
                '--prefix=' + join(build_dir, 'install'),
                '--default-library=static',
                _env=env
            )
            shprint(sh.Command('ninja'), '-C', 'builddir', _env=env)
            shprint(sh.Command('ninja'), '-C', 'builddir', 'install', _env=env)

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['CFLAGS'] += ' -fPIC'
        return env


recipe = LibthorvgRecipe()
