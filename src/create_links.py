from tools import link_launcher, link_process, PARENT_DIR

print("Creating shortcuts...")
link_launcher(True)
link_process()
print("\nDone.")

input()