from PIL import Image
gearIcon = Image.open("canvas_gear.png")
refreshIcon = Image.open("canvas_refresh.png")
newSize = (50, 50)
gearIcon = gearIcon.resize(newSize)
refreshIcon = refreshIcon.resize(newSize)

print(gearIcon.mode)
print(refreshIcon.mode)

gearIcon.show()