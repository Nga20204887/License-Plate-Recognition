import os 
f=open('test.txt','w')
for file in os.listdir("data/licenseplate/val/images"):
    f.write(f"/{file}\n")