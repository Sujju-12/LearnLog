# Example: Linux Foundation course session

Use one **public** entry per module (or per week), not one file for the whole
course. That gives GitHub a visible timeline.

```bash
learnlog add \
  --visibility public \
  --title "LFS101x: Users, groups, and permissions" \
  --summary "How Linux maps users to UIDs, and how chmod/umask control access." \
  --date 2026-08-24 \
  --topic linux --topic linux-foundation \
  --skill chmod --skill umask --skill permissions \
  --type course --type hands-on \
  --resource "Linux Foundation|course|Introduction to Linux (LFS101x)|https://training.linuxfoundation.org/training/introduction-to-linux/" \
  --understanding "Permissions are bits on the inode, not a separate ACL unless you enable ACLs." \
  --concept "UID/GID" --concept "umask" --concept "chmod" \
  --hands-on "Created a user, set umask 027, verified new-file mode." \
  --gaps "When to use POSIX ACLs vs groups." \
  --next "Complete the LFS101x processes and jobs module."

learnlog publish
git add data/entries PROGRESS.md
git commit -m "Learn: LFS101x users and permissions"
git push
```

When you finish the course:

```bash
learnlog achievement add \
  --visibility public \
  --title "Introduction to Linux (LFS101x)" \
  --provider "Linux Foundation" \
  --date 2026-09-15 \
  --url "https://www.credly.com/" \
  --topic linux \
  --skill linux-fundamentals \
  --notes "Completed Linux Foundation Introduction to Linux."
```
