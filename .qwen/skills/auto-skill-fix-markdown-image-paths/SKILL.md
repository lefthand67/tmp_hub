---
name: fix-markdown-image-paths
description: Resolve image rendering issues in Markdown files caused by spaces in directory names by renaming folders to snake_case and updating references.
source: auto-skill
extracted_at: '2026-06-15T13:00:00.000Z'
---

When Markdown images fail to render due to spaces in the file or directory paths, the most robust solution is to rename the directories to a space-free format (like snake_case) and update the references in the document.

### Procedure

1. **Verify Paths**: Compare the image paths in the `.md` file with the actual directory structure on disk using `list_directory` or `ls`.
2. **Confirm File Existence**: Use `glob` or `grep` to ensure the image files actually exist in the project, as they might be missing entirely.
3. **Rename Directory**: Rename the image folder to a name without spaces.
   - *Example*: `My Image Folder` $\rightarrow$ `my_image_folder`
4. **Update References**: Replace all occurrences of the old path with the new path in the Markdown file.
5. **Handle Missing Assets**: If images are missing from the disk despite being referenced, notify the user.

### Why not just URL-encode?
While replacing spaces with `%20` can work in some renderers, renaming the folder to a standard filesystem-friendly format is more portable and prevents issues across different Markdown viewers and OS environments.
