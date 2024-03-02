

class ViewData:
    wreck_list_a = None
    wreck_list_b = None
    scale_multiplier = None
    texture_type = None
    br_link = None

    def sanitise_input(self):
        """
        Sanitises the input
        :return: self
        """
        if self.scale_multiplier is None:
            self.scale_multiplier = 1.0
        else:
            self.scale_multiplier = float(self.scale_multiplier)

        if self.texture_type is None:
            self.texture_type = 'ship'
        else:
            self.texture_type = self.texture_type
