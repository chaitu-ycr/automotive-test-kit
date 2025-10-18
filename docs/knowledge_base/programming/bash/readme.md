# Linux Bash Shell Scripting Tutorial

Welcome to the Bash shell scripting tutorial! This guide introduces the basics and essential concepts of Bash scripting for Linux, inspired by the structure of the Python programming documentation.

---

## 1. Introduction
Bash (Bourne Again SHell) is a popular command-line interpreter for Linux. Bash scripts automate tasks, manage files, monitor systems, and perform deployments efficiently in real-world environments.

## 2. Basic Syntax
- Scripts start with a shebang: `#!/bin/bash`
- Each command is written on a new line.
- Comments start with `#`.

**Use Case:** Automate a daily backup task.
```bash
#!/bin/bash
# Daily backup script
tar -czf /backup/home_$(date +%F).tar.gz /home/user/
```

## 3. Variables
- Assign with `=` (no spaces): `name="Alice"`
- Access with `$`: `echo $name`

**Use Case:** Store and use environment-specific values.
```bash
backup_dir="/backup"
tar -czf "$backup_dir/home_$(date +%F).tar.gz" /home/user/
```

## 4. Conditionals (`if`, `elif`, `else`)
**Use Case:** Check if a service is running and restart if not.
```bash
service="nginx"
if systemctl is-active --quiet $service; then
    echo "$service is running."
else
    echo "$service is not running. Restarting..."
    systemctl restart $service
fi
```

## 5. Loops
### For Loop
**Use Case:** Process multiple log files.
```bash
for logfile in /var/log/*.log; do
    gzip "$logfile"
done
```
### While Loop
**Use Case:** Monitor a process until it finishes.
```bash
pid=1234
while kill -0 $pid 2>/dev/null; do
    echo "Process $pid is still running."
    sleep 5
done
```

## 6. Functions
**Use Case:** Reusable deployment steps.
```bash
deploy_app() {
    git pull
    systemctl restart app
}
deploy_app
```

## 7. Input/Output
- Read input: `read variable`
- Output: `echo $variable`

**Use Case:** Interactive script for user confirmation.
```bash
echo "Do you want to proceed with cleanup? (y/n)"
read answer
if [ "$answer" = "y" ]; then
    rm -rf /tmp/*
    echo "Cleanup done."
else
    echo "Cleanup aborted."
fi
```

## 8. String Manipulation
**Use Case:** Format filenames and extract extensions.
```bash
filename="report_2025.csv"
echo ${filename%.csv}   # Output: report_2025
echo ${filename##*.}    # Output: csv
```

## 9. Arrays
**Use Case:** Batch restart multiple services.
```bash
services=(nginx redis postgresql)
for svc in "${services[@]}"; do
    systemctl restart $svc
done
```

## 10. Error Handling
- Use `set -e` to exit on error.
- Check exit status: `$?`

**Use Case:** Stop script on failure and log errors.
```bash
set -e
cp /important/file /backup/ || echo "Backup failed!" >> /var/log/backup_errors.log
```

## 11. Script Arguments
- `$1`, `$2`, ... for positional arguments.
- `$#` for argument count.

**Use Case:** Parameterize deployment environments.
```bash
# Usage: ./deploy.sh staging
env="$1"
echo "Deploying to $env environment..."
```

## 12. Useful Commands
Here are some commonly used Bash commands with real-world use cases:

- `grep`: Search for error logs in production systems
  ```bash
  grep -i "critical" /var/log/syslog | tail -n 20
  # Find last 20 critical errors in system logs
  ```
- `awk`: Generate a report of disk usage per user
  ```bash
  df -h | awk 'NR>1 {print $1, $5}'
  # Show filesystem and usage percentage
  ```
- `sed`: Bulk update configuration files
  ```bash
  sed -i 's/MaxClients 100/MaxClients 200/g' /etc/httpd/conf/httpd.conf
  # Update Apache MaxClients setting
  ```
- `cut`: Extract usernames from /etc/passwd
  ```bash
  cut -d: -f1 /etc/passwd | sort | uniq
  # List all unique usernames
  ```
- `find`: Clean up old backup files
  ```bash
  find /backups -type f -name "*.bak" -mtime +30 -exec rm {} \;
  # Delete .bak files older than 30 days
  ```
- `xargs`: Restart services listed in a file
  ```bash
  cat services.txt | xargs -I {} systemctl restart {}
  # Restart each service listed in services.txt
  ```
- `sort`/`uniq`: Analyze web server access logs for unique IPs
  ```bash
  awk '{print $1}' access.log | sort | uniq -c | sort -nr | head
  # Top IPs by request count
  ```
- `tr`: Normalize data for import
  ```bash
  cat data.csv | tr -d '\r' > clean_data.csv
  # Remove carriage returns for Linux compatibility
  ```
- `wc`: Monitor file growth in log rotation
  ```bash
  wc -l /var/log/app.log
  # Check number of lines in log file
  ```
- `head`/`tail`: Debugging application startup
  ```bash
  head -n 50 /var/log/app.log
  tail -f /var/log/app.log
  # View first 50 lines and follow log output
  ```
- `chmod`: Secure deployment scripts
  ```bash
  chmod 700 deploy.sh
  # Only owner can execute
  ```
- `chown`: Fix permissions after file transfer
  ```bash
  sudo chown -R appuser:appgroup /var/www/app
  # Set correct ownership for web app files
  ```
- `curl`/`wget`: Health check for REST APIs
  ```bash
  curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health
  # Get HTTP status code for health endpoint
  ```
- `tar`: Archive logs before cleanup
  ```bash
  tar -czvf logs_$(date +%F).tar.gz /var/log/app/
  # Archive logs with date in filename
  ```
- `zip`/`unzip`: Distribute code artifacts
  ```bash
  zip -r release.zip src/ docs/
  unzip release.zip -d /opt/app
  # Package and extract release files
  ```

## 13. Advanced Topics
### Piping and Redirection
- Chain commands for data processing in ETL pipelines:
  ```bash
  cat raw_data.csv | grep -v "ERROR" | awk -F, '{print $2,$5}' | sort > processed_data.txt
  # Filter, extract, and sort data for analytics
  ```
- Redirect error output for troubleshooting:
  ```bash
  ./deploy.sh > deploy.log 2>&1
  # Save both stdout and stderr to log file
  ```

### Background Processes
- Run nightly batch jobs without blocking terminal:
  ```bash
  ./nightly_backup.sh &
  disown
  # Start backup in background and detach from shell
  ```
- Monitor background jobs during system maintenance:
  ```bash
  jobs
  fg %1
  # List and bring backup job to foreground
  ```

### Scheduling (cron)
- Automate database backups:
  ```cron
  0 2 * * * /usr/local/bin/db_backup.sh >> /var/log/db_backup.log 2>&1
  # Run backup at 2 AM daily and log output
  ```
- Send daily status email:
  ```cron
  8 7 * * * /usr/local/bin/send_status.sh | mail -s "Daily Status" admin@example.com
  # Email status report every morning
  ```

### Subshells and Command Substitution
- Deploy to multiple environments:
  ```bash
  for env in dev staging prod; do
    (cd /var/www/$env && git pull)
  done
  # Update code in each environment directory
  ```
- Dynamic configuration loading:
  ```bash
  config_file=$(ls /etc/app/config_*.yml | head -n1)
  echo "Using config: $config_file"
  # Select latest config file automatically
  ```

### Regular Expressions
- Validate input data in scripts:
  ```bash
  if [[ "$email" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "Valid email"
  else
    echo "Invalid email"
  fi
  # Email format validation
  ```
- Extract version numbers from release notes:
  ```bash
  grep -Eo "v[0-9]+\.[0-9]+\.[0-9]+" release_notes.txt
  # Find all semantic version strings
  ```

## 14. References
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [ShellCheck](https://www.shellcheck.net/)

---

*For more examples and use cases, explore the documentation and try writing your own scripts!*
