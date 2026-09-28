from os.path import join
from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory, shprint
import sh


class LibffiRecipe(Recipe):
    version = '3.3'
    url = 'https://github.com/libffi/libffi/archive/refs/tags/v{version}.tar.gz'
    patches = []
    depends = []

    def should_build(self, arch):
        return True

    def get_include_dirs(self, arch):
        # возвращаем путь, куда libffi кладёт заголовки
        return [join(self.get_build_dir(arch.arch), 'install', 'include')]

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(
                sh.Command('./autogen.sh'),
                _env=env
            )
            shprint(
                sh.Command('./configure'),
                '--host=' + arch.command_prefix,
                '--prefix=' + self.get_build_dir(arch.arch) + '/install',
                '--disable-shared',
                '--enable-static',
                '--disable-builddir',
                _env=env
            )
            shprint(sh.Command('make'), '-j4', _env=env)
            shprint(sh.Command('make'), 'install', _env=env)

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['CFLAGS'] += ' -fPIC'
        return env


recipe = LibffiRecipe()
