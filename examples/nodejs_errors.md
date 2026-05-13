# Node.js Error Examples

Real-world Node.js and npm errors and how `heal` helps fix them.

### Error
```bash
$ node app.js
Error: Cannot find module 'express'
Require stack:
- /home/user/project/app.js
    at Function.Module._resolveFilename (internal/modules/cjs/loader.js:815:15)
```

### Using heal
```bash
$ node app.js 2>&1 | heal
```

### Expected Solution
```
The Express module is not installed in your project.

**Solution:**

1. Install the missing module:
   ```bash
   npm install express
   ```

2. If you have a package.json, install all dependencies:
   ```bash
   npm install
   ```

3. Check if node_modules exists:
   ```bash
   ls -la node_modules/
   ```

4. If using yarn:
   ```bash
   yarn install
   ```
```

### Error
```bash
$ npm install
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! Found: react@18.0.0
npm ERR! Could not resolve dependency:
npm ERR! peer react@"^17.0.0" from react-router-dom@5.3.0
```

### Using heal
```bash
$ npm install 2>&1 | heal
```

### Expected Solution
```
There's a peer dependency conflict between React versions.

**Solution (choose one):**

1. Use --legacy-peer-deps flag (quick fix):
   ```bash
   npm install --legacy-peer-deps
   ```

2. Use --force flag (not recommended):
   ```bash
   npm install --force
   ```

3. **Best solution**: Update react-router-dom to a version compatible with React 18:
   ```bash
   npm install react-router-dom@latest
   ```

4. Or downgrade React to version 17:
   ```bash
   npm install react@17 react-dom@17
   ```

5. Check for updated versions:
   ```bash
   npm outdated
   ```
```

### Error
```bash
$ npm start
Error: listen EADDRINUSE: address already in use :::3000
    at Server.setupListenHandle [as _listen2] (net.js:1318:16)
```

### Using heal
```bash
$ npm start 2>&1 | heal
```

### Expected Solution
```
Port 3000 is already being used by another process.

**Solution:**

1. Find and kill the process using port 3000:
   ```bash
   # On Linux/Mac
   lsof -ti:3000 | xargs kill -9
   
   # Or find the process first
   lsof -i :3000
   kill -9 <PID>
   ```

2. On Windows:
   ```bash
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   ```

3. Use a different port:
   ```bash
   PORT=3001 npm start
   ```

4. Or update your .env file:
   ```
   PORT=3001
   ```
```

### Error
```bash
$ npm install my-private-package
npm ERR! code E404
npm ERR! 404 Not Found - GET https://registry.npmjs.org/my-private-package
npm ERR! 404  'my-private-package@latest' is not in the npm registry.
```

### Using heal
```bash
$ npm install my-private-package 2>&1 | heal
```

### Expected Solution
```
The package doesn't exist in the public npm registry or you don't have access.

**Solution:**

1. Check if the package name is correct:
   ```bash
   npm search my-private-package
   ```

2. If it's a private package, login to npm:
   ```bash
   npm login
   npm install my-private-package
   ```

3. If using a private registry, configure it:
   ```bash
   npm config set registry https://your-registry.com
   # or use .npmrc file
   ```

4. If it's a scoped package, ensure proper authentication:
   ```bash
   npm config set @yourscope:registry https://npm.pkg.github.com
   npm config set //npm.pkg.github.com/:_authToken YOUR_TOKEN
   ```
```

### Error
```bash
$ npm run build
> webpack --mode production

sh: 1: webpack: not found
npm ERR! code ELIFECYCLE
npm ERR! syscall spawn
```

### Using heal
```bash
$ npm run build 2>&1 | heal
```

### Expected Solution
```
Webpack is not installed or not found in PATH.

**Solution:**

1. Install webpack as a dev dependency:
   ```bash
   npm install --save-dev webpack webpack-cli
   ```

2. Or install all dependencies:
   ```bash
   npm install
   ```

3. Use npx to run webpack:
   ```bash
   npx webpack --mode production
   ```

4. Update package.json scripts to use npx:
   ```json
   {
     "scripts": {
       "build": "npx webpack --mode production"
     }
   }
   ```
```

### Error
```bash
$ node app.js
/home/user/project/app.js:5
const data = await fetchData();
             ^^^^^
SyntaxError: await is only valid in async function
```

### Using heal
```bash
$ node app.js 2>&1 | heal
```

### Expected Solution
```
You're using `await` outside of an async function.

**Solution:**

1. Wrap your code in an async function:
   ```javascript
   async function main() {
     const data = await fetchData();
     console.log(data);
   }
   
   main().catch(console.error);
   ```

2. Or use top-level await (Node.js 14.8+) with ES modules:
   ```javascript
   // In package.json, add:
   {
     "type": "module"
   }
   
   // Then you can use top-level await
   const data = await fetchData();
   ```

3. Or use .then() instead:
   ```javascript
   fetchData().then(data => {
     console.log(data);
   }).catch(console.error);
   ```
```

### Error
```bash
$ npm install -g typescript
npm ERR! code EACCES
npm ERR! syscall mkdir
npm ERR! path /usr/local/lib/node_modules/typescript
npm ERR! errno -13
npm ERR! Error: EACCES: permission denied
```

### Using heal
```bash
$ npm install -g typescript 2>&1 | heal
```

### Expected Solution
```
You don't have permission to install global packages in the system directory.

**Solution (choose one):**

1. **Recommended**: Use a Node version manager (nvm):
   ```bash
   # Install nvm
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   
   # Install Node.js with nvm
   nvm install node
   
   # Now you can install global packages without sudo
   npm install -g typescript
   ```

2. Change npm's default directory:
   ```bash
   mkdir ~/.npm-global
   npm config set prefix '~/.npm-global'
   echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
   source ~/.bashrc
   npm install -g typescript
   ```

3. Use sudo (not recommended):
   ```bash
   sudo npm install -g typescript
   ```

4. Install locally instead:
   ```bash
   npm install --save-dev typescript
   npx tsc --version
   ```
```

### Error
```bash
$ npm run build
FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed 
- JavaScript heap out of memory
```

### Using heal
```bash
$ npm run build 2>&1 | heal
```

### Expected Solution
```
Node.js ran out of memory during the build process.

**Solution:**

1. Increase Node.js memory limit:
   ```bash
   export NODE_OPTIONS="--max-old-space-size=4096"
   npm run build
   ```

2. Update package.json script:
   ```json
   {
     "scripts": {
       "build": "node --max-old-space-size=4096 node_modules/.bin/webpack"
     }
   }
   ```

3. For Windows:
   ```bash
   set NODE_OPTIONS=--max-old-space-size=4096
   npm run build
   ```

4. Optimize your build:
   - Enable production mode
   - Remove source maps in production
   - Use code splitting
   - Check for memory leaks in your code
```
