
def extract_cleaned_patches(files):
    patches=[]
    for file in files:
        if 'patch' in file:
            patches.append({
                'filename':file['filename'],
                'patch':file['patch']
            })
    clean_patches = []
    for p in patches:
        if len(p["patch"]) < 4000:
            clean_patches.append(p)
    return clean_patches