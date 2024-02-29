## zkillBattleVis
A tool to visualize zkillboard losses in the position of the system they were lost in.
Currently it will only work within one grid and displays the loss coordinates as a 3D object.

![Screenshot](screenshot2.png)


---

### How does it work?

- When running main.py currently...
- It will take a list of zkillboard links, strip the ID out, and create Wreck objects.
- Wreck objects contain all the info about the wreck, including coordinates.
- The tool then scales coordinates down to their locals by running modulo and taking the last few digits.
- Scaling down further by 2000 brings them to a reasonable size for the window.
- The coordinate are then plotted (as cats, fish, or cubes, not wrecks yet) on the window.

Alt or Cmd+Tab out when starting to resolve a bug with the camera.
You can then click back in and hold right click to bind the mouse to the window. (so you can fly).

WASD controls the flight. Press Esc to quit.

---

### What creates the 3D scene?

- The 3D scene is created using Pygame and PyOpenGL.
- The 3D scene is rendered using a ton of vector maths and a perspective projection matrix.
- [Follow this tutorial to recreate something like this](https://www.youtube.com/watch?v=eJDIsFJN4OQ) 


---

### To Do (eventually...)

- [ ] Add a better wreck model
- [ ] Add camera control hints to the screen
- [ ] Add a skybox
- [ ] Add another model to the screen so you can better understand the scale
- [ ] Improve the lighting
- [ ] Fix the bug with the camera not capturing right click on start

---

**Cats!**
![Screenshot](screenshot1.png)