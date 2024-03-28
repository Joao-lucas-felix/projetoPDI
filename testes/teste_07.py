from Util.Util import read_mask_from_file




mask = read_mask_from_file("masks/media.txt")

print(mask.size)
for line in mask.matriz:
    print(line)