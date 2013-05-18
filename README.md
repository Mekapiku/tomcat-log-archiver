# Tomcat Log Archiver

## usage
```python
def get_archive_name(dir_list):
    return "~/backup/archive"

archiver = LogArchiver(/var/log/tomcat6)

pattern = re.compile(r'.*\.log')
archiver.archive(pattern, get_archive_name, "zip")
```
