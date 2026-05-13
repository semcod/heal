# Docker Error Examples

Real-world Docker errors and how `heal` helps fix them.

### Error
```bash
$ docker run -p 8080:80 nginx
docker: Error response from daemon: driver failed programming external connectivity 
on endpoint nginx: Bind for 0.0.0.0:8080 failed: port is already allocated.
```

### Using heal
```bash
$ docker run -p 8080:80 nginx 2>&1 | heal
```

### Expected Solution
```
Port 8080 is already being used by another process on your system.

**Solution (choose one):**

1. Find and stop the process using port 8080:
   ```bash
   # Find the process
   sudo lsof -i :8080
   # or
   sudo netstat -tulpn | grep :8080
   
   # Kill the process (replace PID with actual process ID)
   kill -9 <PID>
   ```

2. Use a different port:
   ```bash
   docker run -p 8081:80 nginx
   ```

3. Stop the conflicting Docker container:
   ```bash
   docker ps | grep 8080
   docker stop <container_id>
   ```
```

### Error
```bash
$ docker build -t myapp .
Step 5/10 : COPY requirements.txt /app/
COPY failed: file not found in build context or excluded by .dockerignore: 
stat requirements.txt: file does not exist
```

### Using heal
```bash
$ docker build -t myapp . 2>&1 | heal
```

### Expected Solution
```
Docker cannot find `requirements.txt` in the build context.

**Solution:**

1. Verify the file exists in your current directory:
   ```bash
   ls -la requirements.txt
   ```

2. Check your .dockerignore file - make sure requirements.txt isn't excluded:
   ```bash
   cat .dockerignore
   ```

3. If the file is in a subdirectory, update your Dockerfile:
   ```dockerfile
   COPY ./path/to/requirements.txt /app/
   ```

4. Make sure you're running docker build from the correct directory:
   ```bash
   cd /path/to/project
   docker build -t myapp .
   ```
```

### Error
```bash
$ docker run myapp
mkdir: cannot create directory '/app/data': Permission denied
```

### Using heal
```bash
$ docker run myapp 2>&1 | heal
```

### Expected Solution
```
The container process doesn't have permission to create directories.

**Solution:**

1. Run container as root (not recommended for production):
   ```bash
   docker run --user root myapp
   ```

2. **Better**: Fix permissions in Dockerfile:
   ```dockerfile
   FROM python:3.9
   
   # Create app directory with proper permissions
   RUN mkdir -p /app/data && chmod 777 /app/data
   
   # Or create a non-root user
   RUN useradd -m appuser
   RUN chown -R appuser:appuser /app
   USER appuser
   ```

3. Use a volume with proper permissions:
   ```bash
   docker run -v $(pwd)/data:/app/data myapp
   ```
```

### Error
```bash
$ docker-compose up
ERROR: Network myapp_default declared as external, but could not be found. 
Please create the network manually using `docker network create myapp_default` 
and try again.
```

### Using heal
```bash
$ docker-compose up 2>&1 | heal
```

### Expected Solution
```
Docker Compose is looking for an external network that doesn't exist.

**Solution (choose one):**

1. Create the network manually:
   ```bash
   docker network create myapp_default
   docker-compose up
   ```

2. Remove the external network declaration from docker-compose.yml:
   ```yaml
   # Remove or comment out:
   networks:
     default:
       external: true
   ```

3. Let Docker Compose create the network automatically:
   ```yaml
   networks:
     default:
       driver: bridge
   ```
```

### Error
```bash
$ docker run mycompany/myapp:latest
Unable to find image 'mycompany/myapp:latest' locally
docker: Error response from daemon: pull access denied for mycompany/myapp, 
repository does not exist or may require 'docker login'
```

### Using heal
```bash
$ docker run mycompany/myapp:latest 2>&1 | heal
```

### Expected Solution
```
Docker cannot find the image locally or remotely.

**Solution:**

1. If it's a private image, login first:
   ```bash
   docker login
   # Enter your credentials
   docker run mycompany/myapp:latest
   ```

2. If you need to build the image first:
   ```bash
   docker build -t mycompany/myapp:latest .
   docker run mycompany/myapp:latest
   ```

3. Check if the image name is correct:
   ```bash
   docker images | grep myapp
   ```

4. Pull from the correct registry:
   ```bash
   docker pull registry.example.com/mycompany/myapp:latest
   ```
```

### Error
```bash
$ docker build -t myapp .
failed to register layer: Error processing tar file(exit status 1): 
write /usr/local/lib/python3.9/site-packages/...: no space left on device
```

### Using heal
```bash
$ docker build -t myapp . 2>&1 | heal
```

### Expected Solution
```
Docker has run out of disk space.

**Solution:**

1. Clean up unused Docker resources:
   ```bash
   # Remove unused containers, networks, images
   docker system prune -a
   
   # Remove unused volumes (be careful!)
   docker volume prune
   ```

2. Check disk usage:
   ```bash
   df -h
   docker system df
   ```

3. Remove specific unused images:
   ```bash
   docker images
   docker rmi <image_id>
   ```

4. Remove stopped containers:
   ```bash
   docker container prune
   ```

5. If using Docker Desktop, increase disk allocation in settings.
```

### Error
```bash
$ docker run -d myapp
a1b2c3d4e5f6
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### Using heal
```bash
$ docker logs a1b2c3d4e5f6 2>&1 | heal
```

### Expected Solution
```
The container started but exited immediately. Check the logs for the reason.

**Solution:**

1. View container logs:
   ```bash
   docker logs <container_id>
   ```

2. Run container in foreground to see errors:
   ```bash
   docker run myapp
   ```

3. Common issues:
   - Application crashed on startup
   - Missing environment variables
   - Wrong CMD/ENTRYPOINT in Dockerfile

4. Keep container running for debugging:
   ```bash
   docker run -it myapp /bin/bash
   ```

5. Check if the main process exits too quickly:
   ```dockerfile
   # In Dockerfile, ensure CMD runs a long-lived process
   CMD ["python", "app.py"]  # Not a script that exits immediately
   ```
```
