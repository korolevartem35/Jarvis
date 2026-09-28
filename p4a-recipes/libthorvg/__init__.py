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
            # Патчим meson.build — убираем проблему с clang_lib_dir
            meson_file = join(build_dir, 'meson.build')
            if not self._meson_patched(meson_file):
                with open(meson_file, 'r') as f:
                    content = f.read()
                # Заменяем проблемную секцию на фиктивную
                content = content.replace(
                    "clang_lib_dir = glob(pattern)[0]",
                    "clang_lib_dir = ''"
                )
                with open(meson_file, 'w') as f:
                    f.write(content)

            shprint(
                sh.Command('meson'),
                'setup',
                '--cross-file', 'tmp/android.meson.cross',
                '--prefix=' + join(build_dir, 'install'),
                '--default-library=static',
                _env=env
            )
            shprint(sh.Command('ninja'), '-C', 'builddir', _env=env)
            shprint(sh.Command('ninja'), '-C', 'builddir', 'install', _env=env)

    def _meson_patched(self, path):
        try:
            with open(path, 'r') as f:
                return 'clang_lib_dir = \'\'' in f.read()
        except Exception:
            return False

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['CFLAGS'] += ' -fPIC'
        return env


recipe = LibthorvgRecipe()
