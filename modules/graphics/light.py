import glm


class Light:
    def __init__(self, position=(0, 0, 4), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.Ia = 0.2 * self.color  # Ambient light
        self.Id = 0.6 * self.color  # Diffuse light
        self.Is = 0.5 * self.color  # Specular light
