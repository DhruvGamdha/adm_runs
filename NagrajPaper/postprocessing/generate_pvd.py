### In order to run, copy the file in the directory where the results folder are location and run it as:
### python gen_pvd.py
### It should print paraview_vel.pvd, paraview_p.pvd, paraview_ch.pvd which can be loaded direcly on Paraview / Visit
### Author : Boshun Gao

import os
import sys
import glob
startpath = os.path.dirname(os.path.realpath(__file__))
folders = []
# print(sys.argv)
# print(startpath)
res = []
for root, dirs, files in os.walk(startpath):
    for f in [f for f in files if f.endswith(".pvtu")]:
        res.append((root, f))
res = sorted(res, key=lambda x: x[1])
vel_res = [r for r in res if "diffusivity" in r[1]]

marker_res = [r for r in res if "value" in r[1]]

bdr_res = [r for r in res if "bdr" in r[1]]
# ch_res = [r for r in res if "ch" in r[1]]
# if "all" arguments passed

if len(sys.argv) == 2 and sys.argv[1] == "all":
    pass
else:
    # print(vel_res)
    # no arguments, only this directory
    vel_res = [r for r in res if "diffusivity_" in r[1] and os.path.dirname(r[0]) == startpath]
    marker_res = [r for r in res if "value_" in r[1] and os.path.dirname(r[0]) == startpath]
    bdr_res = [r for r in res if "bdr_" in r[1] and os.path.dirname(r[0]) == startpath]
    # p_res = [r for r in res if "p_" in r[1] and os.path.dirname(r[0]) == startpath]
    # ch_res = [r for r in res if "ch_" in r[1] and os.path.dirname(r[0]) == startpath]
print(vel_res)
def write_pvd_file(name, res):
    def res_to_ts(res):
        return int(res.replace(".pvtu", "").split("_")[-1])

    print(res)
    if len(res) > 0:
        with open(os.path.join(startpath, name), "w") as f:
            f.write(r"""<?xml version="1.0"?>
<VTKFile type="Collection" version="0.1"
         byte_order="LittleEndian"
         compressor="vtkZLibDataCompressor">
<Collection>
""")


            for r in res:
                # print("r[0] :" + r[0])
                # print("r[1] :" + r[1])
                # # Get text from r[0] from the end till data/
                # print("Extraction   :"+r[0][r[0].rfind("data/") + 5:])
                relativePath = r[0][r[0].rfind("data/") + 5:] + "/" + r[1]
                print("relativePath :" + relativePath)
                f.write("<DataSet timestep=\"{ts}\" group=\"\" part=\"0\" file=\"{f}\"/>\n".format(ts=res_to_ts(r[1]), f=relativePath))#os.path.join(r[0], r[1])))
            f.write(r"""
  </Collection>
</VTKFile>
""")
write_pvd_file("paraview_ch.pvd", vel_res)
write_pvd_file("paraview_marker.pvd", marker_res)
write_pvd_file("paraview_bdr.pvd", bdr_res)
# write_pvd_file("paraview_p.pvd", p_res)
# write_pvd_file("paraview_ch.pvd", ch_res)