import cPickle
import numpy as np
MEMBERS = [
    'binding', 'binding_rows', 'binding_cols',
    'pattern', 'pattern_repeat_x', 'pattern_repeat_y'
]


def save_models(filename, mainwindow):
    # Data
    binding = mainwindow.binding
    pattern = mainwindow.pattern
    pattern_repeat_x = mainwindow.pattern_repeat_x
    pattern_repeat_y = mainwindow.pattern_repeat_y

    # Quick and dirty serialization.
    np.savez(
        filename,
        binding_data=binding.data,
        binding_padding=binding.padding,
        binding_size=binding.size,
        pattern_repeat_x=pattern_repeat_x,
        pattern_repeat_y=pattern_repeat_y,
        pattern_data=pattern.data,
        pattern_padding=pattern.padding,
        pattern_size=pattern.size,
        pattern_hor_colors=pattern.hor_colors,
        pattern_ver_colors=pattern.ver_colors
    )


def load_models(filename, mainwindow):
    data = np.load(filename)

    binding = mainwindow.binding
    binding.padding = tuple(data['binding_padding'])
    binding.size = tuple(data['binding_size'])
    binding.data = data['binding_data']

    pattern = mainwindow.pattern
    pattern.padding = tuple(data['pattern_padding'])
    pattern.size = tuple(data['pattern_size'])
    pattern.data = data['pattern_data']
    pattern.hor_colors = data['pattern_hor_colors']
    pattern.ver_colors = data['pattern_ver_colors']

    mainwindow.trait_setq(pattern=pattern)
    mainwindow.trait_setq(binding=binding)
    mainwindow.trait_set(binding_rows=binding.data.shape[0])
    mainwindow.trait_set(binding_cols=binding.data.shape[1])
    mainwindow.trait_set(pattern_repeat_x=data['pattern_repeat_x'])
    mainwindow.trait_set(pattern_repeat_y=data['pattern_repeat_y'])
