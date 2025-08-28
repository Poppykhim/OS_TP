# Safe `rm` and `restore` System

## How the Scripts Work

- **rm (safe delete):**  
  Replaces the default `rm` command. Instead of permanently deleting files, it moves them to `/tmp/trash/` with a timestamp added to avoid name conflicts. Each deletion is logged in `/tmp/trash/trash.log`, which records:

  - Original file path
  - Trash file path
  - Timestamp of deletion

- **restore (recover):**  
  Restores files or directories from the trash. It searches the log for the most recent match, recreates the destination folder if needed, and moves the file/directory back to its original location.

---

## 🛠️ How to Use

1. **Delete a file safely:**
   ```bash
   rm filename
   ```
2. **Check the trash contents:**

   ```bash
   ls /tmp/trash/
   cat /tmp/trash/trash.log
   ```

3. **Restore a file or folder:**

   ```bash
   restore filename
   ls
   ```
