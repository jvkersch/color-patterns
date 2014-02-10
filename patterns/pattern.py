import numpy as np

from traits.api import Array, HasTraits, Property, cached_property

from utility import lcm


class Pattern(HasTraits):

    # The binding for this pattern.
    binding = Array

    # Color model for the x-direction.
    x_colors = Array

    # Color model for the y-direction.
    y_colors = Array

    # Pattern data (read-only property)
    pattern = Property(Array, depends_on="binding, x_colors, y_colors")

    ### Traits getters/setters ###############################################

    @cached_property
    def _get_pattern(self):

        binding_x_size, binding_y_size = self.binding.shape
        x_col_size = self.x_colors.shape[0]
        y_col_size = self.y_colors.shape[0]

        x_size = lcm(x_col_size, binding_x_size)
        y_size = lcm(y_col_size, binding_y_size)

        pattern_data = np.empty((x_size, y_size, 3))
        for k in xrange(x_size):
            for l in xrange(y_size):
                if self.binding[k % binding_x_size, l % binding_y_size]:
                    color = self.x_colors[k % x_col_size]
                else:
                    color = self.y_colors[l % y_col_size]
                pattern_data[k, l, :] = color

        return pattern_data
