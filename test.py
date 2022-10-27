import subprocess


project_dir = "/Users/antonio/Documents/Projects/Web/TST_Test"
subprocess.Popen(["make", "init"], stdout=subprocess.PIPE, cwd=project_dir)
