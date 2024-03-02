#version 330 core

layout (location = 0) in vec3 in_position;

out vec3 texCubeCoords;

uniform mat4 m_projection;
uniform mat4 m_view;

void main()
{
    texCubeCoords = in_position;
    vec4 pos = m_projection * m_view * vec4(in_position, 1.0);
    gl_Position = pos.xyww;
    gl_Position.z -= 0.0001;
}
